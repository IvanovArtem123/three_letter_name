from fastapi import HTTPException


def error(status_code: int, message: str) -> HTTPException:
    """Возвращает Исключение ошибки с детальной информацией."""
    return HTTPException(
        status_code=status_code,
        detail={'code': status_code, 'message': message}
    )


def bad_request(message: str) -> HTTPException:
    """400 Bad Request."""
    return error(400, message)


def unauthorized(message: str) -> HTTPException:
    """401 Unauthorized."""
    return error(401, message)


def forbidden(message: str) -> HTTPException:
    """403 Forbidden."""
    return error(403, message)


def not_found(message: str) -> HTTPException:
    """404 Not Found."""
    return error(404, message)


def unprocessable(message: str) -> HTTPException:
    """422 Unprocessable Entity."""
    return error(422, message)
