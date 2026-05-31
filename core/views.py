from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from .forms import RecommendationForm
from recommendation.saw import saw_recommendation
from products.models import Product, ProductValue


def home(request):
    form = RecommendationForm()
    return render(request, 'core/home.html', {'form': form})


def recommendation_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    results = []
    form = RecommendationForm()
    show_results = False
    if request.method == 'POST':
        show_results = True
        form = RecommendationForm(request.POST)
        category = request.POST.get('category', '')
        budget = float(request.POST.get('budget', 10000000))
        ram = float(request.POST.get('ram', 8))
        baterai = float(request.POST.get('baterai', 12))
        user_weights = {
            'harga': budget,
            'ram': ram,
            'baterai': baterai
        }
        results = saw_recommendation(user_weights=user_weights, category=category)
    return render(request, 'core/recommendation.html', {
        'form': form,
        'results': results,
        'show_results': show_results
    })

def about(request):
    return render(request, 'core/about.html')


def catalog(request):
    products = Product.objects.select_related('category').all()
    items = []
    for product in products:
        values = ProductValue.objects.filter(product=product).select_related('criteria')
        items.append({'product': product, 'values': values})
    return render(request, 'core/catalog.html', {'items': items})


def register(request):
    error = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            error = 'Email sudah terdaftar.'
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = name
            user.save()
            return redirect('user_login')
    return render(request, 'core/register.html', {'error': error})


def user_login(request):
    error = None
    if request.user.is_authenticated:
        return redirect('beranda')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and not user.is_staff:
            auth_login(request, user)
            return redirect('beranda')
        else:
            error = 'Username atau password salah.'
    return render(request, 'core/user_login.html', {'error': error})


def user_logout(request):
    auth_logout(request)
    return redirect('user_login')

