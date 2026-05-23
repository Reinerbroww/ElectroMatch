from django.shortcuts import render
from .forms import RecommendationForm
from recommendation.services import saw_recommendation

def home(request):
    form = RecommendationForm()
    return render(request, 'core/home.html', {'form': form})

def recommendation_view(request):
    results = []
    form = RecommendationForm()

    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            budget = form.cleaned_data['budget']
            kebutuhan = form.cleaned_data['kebutuhan']

            # kirim ke SAW
            results = saw_recommendation(
                category=category,
                budget=budget,
                kebutuhan=kebutuhan
            )

    return render(request, 'core/recommendation.html', {
        'form': form,
        'results': results
    })