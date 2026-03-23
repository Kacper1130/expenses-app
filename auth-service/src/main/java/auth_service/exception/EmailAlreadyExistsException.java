package auth_service.exception;

import org.springframework.http.HttpStatus;

public class EmailAlreadyExistsException extends BaseException {
    public EmailAlreadyExistsException() {
        super("Podany e-mail został już użyty", HttpStatus.CONFLICT);
    }
}
