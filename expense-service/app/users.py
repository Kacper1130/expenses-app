import httpx
import asyncio

# Prosty cache w pamięci — słownik {user_id: name}
# Dzięki temu nie pytamy auth-service za każdym razem o to samo imię
_name_cache: dict[str, str] = {}
_email_cache: dict[str, str] = {}

AUTH_SERVICE_URL = "http://auth-service:8081"


async def get_user_name(user_id: str) -> str:
    """
    Pobiera imię użytkownika z auth-service po jego UUID.
    Jeśli już mamy w cache — zwraca od razu bez zapytania do sieci.
    Jeśli nie ma — pyta auth-service i zapisuje w cache.
    Jeśli coś pójdzie nie tak — zwraca skróconego UUID jako fallback.
    """
    if user_id in _name_cache:
        return _name_cache[user_id]

    try:
        # httpx to async odpowiednik biblioteki requests
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/api/auth/users/{user_id}")

        if response.status_code == 200:
            data = response.json()
            name = data.get("name") or data.get("email", user_id[:8])
            _name_cache[user_id] = name   # zapisz w cache
            return name

    except Exception:
        pass  # sieć nie działa, auth-service nie odpowiada itp.

    # Fallback — pierwsze 8 znaków UUID żeby nie wyświetlać całego
    return user_id[:8] + "..."

async def get_user_email(user_id: str) -> str | None:
    if user_id in _email_cache:
        return _email_cache[user_id]
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/api/auth/users/{user_id}")
        if response.status_code == 200:
            email = response.json().get("email")
            if email:
                _email_cache[user_id] = email
                return email
    except Exception:
        pass
    return None


async def get_user_emails(user_ids: list[str]) -> list[str]:
    results = await asyncio.gather(*[get_user_email(uid) for uid in user_ids])
    return [email for email in results if email is not None]
