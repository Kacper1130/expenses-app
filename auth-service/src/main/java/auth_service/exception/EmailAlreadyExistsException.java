package auth_service.exception;

import org.springframework.http.HttpStatus;

public class EmailAlreadyExistsException extends BaseException {
    public EmailAlreadyExistsException() {
        super("This email is already registered", HttpStatus.CONFLICT);
    }
}
