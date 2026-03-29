package auth_service.auth;

import auth_service.dto.AuthResponse;
import auth_service.dto.LoginRequest;
import auth_service.dto.RegistrationRequest;
import auth_service.user.User;
import auth_service.user.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
class AuthController {

    private final AuthService authService;
    private final UserService userService;

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody RegistrationRequest request) {
        AuthResponse authResponse = authService.register(request);
        return ResponseEntity.ok(authResponse);
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> authenticate(@RequestBody LoginRequest request) {
        AuthResponse authResponse = authService.login(request);
        return ResponseEntity.ok(authResponse);
    }

    // NOWY endpoint — zwraca imię i email usera po jego UUID
    // Używany wewnętrznie przez expense-service (nie przez frontend bezpośrednio)
    @GetMapping("/users/{id}")
    public ResponseEntity<Map<String, String>> getUserInfo(@PathVariable UUID id) {
        return userService.findById(id)
                .map(user -> ResponseEntity.ok(Map.of(
                        "id",    user.getId().toString(),
                        "name",  user.getName(),
                        "email", user.getEmail()
                )))
                .orElse(ResponseEntity.notFound().build());
    }
}
