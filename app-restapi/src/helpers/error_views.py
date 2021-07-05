from django.http import JsonResponse


def error_404(requet, exception):
    message = 'The endpoint is not found'
    response = JsonResponse(data={'message': message, 'status_code': 404})
    response.status_code = 404
    return response

def error_500(requet):
    message = 'An error occurred, its on us'
    response = JsonResponse(data={'message': message, 'status_code': 500})
    response.status_code = 500
    return response
