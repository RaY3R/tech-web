from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request, 'home/index.html')

def results_view(request):
    context = {
        "user": request.session
    }
    return render(request, 'home/results.html', context)