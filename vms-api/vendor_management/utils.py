from rest_framework.response import Response


# This function is returning the success response
def success_response(data):
    return Response(
        {
            'result': {
                "data": data,
                "message": "success",
                "error": False}
        }
    )


# This function is returning the error response
def error_response(message):
    return Response(
        {
            'result': {
                "data": {},
                "message": message,
                "error": True}
        }
    )
