from django.shortcuts import render
from .services import saw_recommendation

def recommendation_view(request):
    results = saw_recommendation()

    return render(request, 'core/result.html', {
        'results': results
    })