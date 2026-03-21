package auth_service.exception;

import lombok.Getter;
import org.springframework.http.HttpStatus;

@Getter
abstract class BaseException extends RuntimeException {
    private final HttpStatus status;

    protected BaseException(String message, HttpStatus status) {
        super(message);
        this.status = status;
    }
}
