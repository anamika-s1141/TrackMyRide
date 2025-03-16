from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is None:
        logger.error(f"Unhandled exception: {exc}")
        return Response({
            'detail': 'An unexpected error occurred.',
            'type': exc.__class__.__name__
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add more exception details
    if hasattr(response, 'data'):
        if isinstance(response.data, dict):
            response.data['type'] = exc.__class__.__name__
            if hasattr(exc, 'get_full_details'):
                response.data['errors'] = exc.get_full_details()
        else:
            response.data = {
                'detail': response.data,
                'type': exc.__class__.__name__
            }

    return response 