from django.shortcuts import render
from .forms import RecommendationForm
from recommendation.saw import saw_recommendation
from products.models import Product, ProductValue

def home(request):
    form = RecommendationForm()
    return render(request, 'core/home.html', {'form': form})

def recommendation_view(request):
    results = []
    # Inisialisasi form kosong agar dropdown kategori tidak error
    form = RecommendationForm()

    show_results = False
    if request.method == 'POST':
        show_results = True
        form = RecommendationForm(request.POST)
        
        # 1. Menangkap pilihan Kategori dari pengguna
        category = request.POST.get('category', '')

        # 2. Menangkap nilai dari 3 Slider Premium kita
        budget = float(request.POST.get('budget', 10000000))
        ram = float(request.POST.get('ram', 8))
        baterai = float(request.POST.get('baterai', 12))

        # 3. Membungkus nilai slider
        user_weights = {
            'harga': budget,
            'ram': ram,
            'baterai': baterai
        }

        # 4. Mengirim data ke mesin SAW
        results = saw_recommendation(user_weights=user_weights, category=category)

    return render(request, 'core/recommendation.html', {
        'form': form,
        'results': results,
        'show_results': show_results
    })