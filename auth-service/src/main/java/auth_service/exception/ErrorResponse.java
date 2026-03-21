package auth_service.exception;

import java.time.LocalDateTime;

record ErrorResponse(
        int status,
        String message
) {
}
