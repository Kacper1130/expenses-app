package auth_service.exception;

import org.springframework.http.HttpStatus;

public class PasswordsNotMatchException extends BaseException {
    public PasswordsNotMatchException() {
        super("Passwords do not match", HttpStatus.BAD_REQUEST);
    }
}
