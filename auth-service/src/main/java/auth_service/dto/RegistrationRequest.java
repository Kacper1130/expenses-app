package auth_service.dto;

import jakarta.validation.constraints.NotBlank;

// Dodajemy pole "name" — imię podawane przy rejestracji
public record RegistrationRequest(
    @NotBlank String email,
    @NotBlank String password,
    @NotBlank String confirmPassword,
    @NotBlank String name
) {}
