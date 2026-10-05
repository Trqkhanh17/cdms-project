import logging
from functools import wraps

from django.db import DatabaseError, IntegrityError, OperationalError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


logger = logging.getLogger(__name__)


def api_exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except APIException:
            raise

        except IntegrityError as error:
            logger.exception("Database integrity error")
            return Response(
                {
                    "status": "error",
                    "error_code": "INTEGRITY_ERROR",
                    "message": "The data conflicts with an existing record.",
                },
                status=status.HTTP_409_CONFLICT,
            )

        except (OperationalError, DatabaseError) as error:
            logger.exception("Database is unavailable")
            return Response(
                {
                    "status": "error",
                    "error_code": "DATABASE_ERROR",
                    "message": "Database operation failed. Please try again later.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except Exception as error:
            logger.exception("Unexpected API error")
            return Response(
                {
                    "status": "error",
                    "error_code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper