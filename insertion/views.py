from django.http import JsonResponse

# Create your views here.
def index(request, id):
    return JsonResponse({'id': id})