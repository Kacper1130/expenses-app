package auth_service.exception;

record ErrorResponse(
        int status,
        String message
) {
}
