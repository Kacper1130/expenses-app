package auth_service.dto;

public record RegistrationRequest(String email, String password, String confirmPassword) {
}
