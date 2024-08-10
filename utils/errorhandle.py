from django.http import JsonResponse

def handler404(request,exception):
    response = JsonResponse(data={'error':'path not found'})
    response.status_code = 404
    return response