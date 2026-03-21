package auth_service.exception;

import org.springframework.http.HttpStatus;

public class LoginFailedException extends BaseException {
    public LoginFailedException(){
        super("Invalid email or password", HttpStatus.UNAUTHORIZED);
    }
}
