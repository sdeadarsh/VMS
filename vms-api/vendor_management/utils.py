from rest_framework.response import Response


def success_response(data):
    return Response(
        {
            'result': {
                "data": data,
                "message": "success",
                "error": False}
        }
    )


def error_response(message):
    return Response(
        {
            'result': {
                "data": {},
                "message": message,
                "error": True}
        }
    )
