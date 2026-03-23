package auth_service.exception;

import org.springframework.http.HttpStatus;

public class LoginFailedException extends BaseException {
    public LoginFailedException(){
        super("Niepoprawny e-mail lub hasło", HttpStatus.UNAUTHORIZED);
    }
}
