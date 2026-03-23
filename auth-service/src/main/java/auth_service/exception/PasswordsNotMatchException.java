package auth_service.exception;

import org.springframework.http.HttpStatus;

public class PasswordsNotMatchException extends BaseException {
    public PasswordsNotMatchException() {
        super("Hasła nie są takie same", HttpStatus.BAD_REQUEST);
    }
}
