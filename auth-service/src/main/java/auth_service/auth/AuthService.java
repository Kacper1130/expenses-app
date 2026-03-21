package auth_service.auth;

import auth_service.dto.AuthResponse;
import auth_service.dto.LoginRequest;
import auth_service.dto.RegistrationRequest;
import auth_service.exception.LoginFailedException;
import auth_service.exception.PasswordsNotMatchException;
import auth_service.security.CustomUserDetails;
import auth_service.security.JwtUtils;
import auth_service.user.User;
import auth_service.user.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
@RequiredArgsConstructor
class AuthService {

    private final UserService userService;
    private final JwtUtils jwtUtils;
    private final AuthenticationManager authenticationManager;

    public AuthResponse register(RegistrationRequest request) {
        validateRequest(request);
        User user = userService.createUser(request);
        String jwtToken = jwtUtils.generateToken(user.getId());
        return new AuthResponse(jwtToken);
    }

    public AuthResponse login(LoginRequest request) {
        Authentication authentication;
        try {
            authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.email(), request.password())
            );
        } catch (AuthenticationException e) {
            throw new LoginFailedException();
        }

        CustomUserDetails customUserDetails = (CustomUserDetails) authentication.getPrincipal();
        UUID userId = customUserDetails.user().getId();
        String jwtToken = jwtUtils.generateToken(userId);
        return new AuthResponse(jwtToken);
    }

    private void validateRequest(RegistrationRequest request) {
        if (!request.password().equals(request.confirmPassword())) {
            throw new PasswordsNotMatchException();
        }
    }

}
