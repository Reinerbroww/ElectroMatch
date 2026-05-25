from django.shortcuts import render
from .services import saw_recommendation

def recommendation_view(request):
    results = None
    if request.method == "POST":
        # Ambil bobot dari name slider di HTML
        # Kita ambil dari kriteria 'Harga', 'RAM', 'Baterai'
        user_weights = {
            'harga': float(request.POST.get('weight_harga', 3)),
            'ram': float(request.POST.get('weight_ram', 3)),
            'baterai': float(request.POST.get('weight_baterai', 3)),
        }
        results = saw_recommendation(user_weights)
    
    return render(request, 'core/recommendation.html', {'results': results})