import csv
import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product, Category, Criteria, ProductValue
from products.forms import ProductForm, CriteriaForm, ProductValueForm


def admin_login(request):
    error = None
    if request.user.is_authenticated:
        return redirect('dashboard_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_index')
        else:
            error = "Username atau password salah, atau bukan admin."

    return render(request, 'dashboard/login.html', {'error': error})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required(login_url='/login/')
def dashboard_index(request):
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'total_criteria': Criteria.objects.count(),
        'total_values': ProductValue.objects.count(),
        'recent_products': Product.objects.order_by('-id')[:5],
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='/login/')
def download_monthly_report(request):
    today = datetime.date.today()
    month_label = today.strftime('%Y%m')
    month_name = today.strftime('%B %Y')
    filename = f'laporan-bulanan-{month_label}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow([f'LAPORAN BULANAN ELECTROMATCH - {month_name}'])
    writer.writerow([])
    writer.writerow(['ID', 'Nama Produk', 'Kategori', 'Brand', 'Harga', 'Nilai Kriteria SAW'])

    products = Product.objects.select_related('category').all()
    values = ProductValue.objects.select_related('criteria').filter(product__in=products)
    value_map = {}
    for pv in values:
        value_map.setdefault(pv.product_id, []).append(pv)

    for product in products:
        saw_values = value_map.get(product.id, [])
        saw_text = '; '.join([f'{v.criteria.name}: {v.value}' for v in saw_values]) if saw_values else 'N/A'
        writer.writerow([
            product.id,
            product.name,
            product.category.name,
            product.brand,
            product.price,
            saw_text,
        ])

    return response


# ───────────── PRODUCT CRUD ─────────────
@login_required(login_url='/login/')
def dashboard_products(request):
    query = request.GET.get('q', '').strip()
    product_list = Product.objects.select_related('category').all()

    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'dashboard/products.html', {
        'products': products,
        'q': query,
    })


@login_required(login_url='/login/')
def product_add(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('dashboard_products')

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Tambah Produk Baru',
        'button': 'Simpan Produk'
    })


@login_required(login_url='/login/')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    page = request.GET.get('page') or request.POST.get('page')
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produk berhasil diupdate!')
            redirect_url = reverse('dashboard_products')
            if page:
                redirect_url += f'?page={page}'
            return redirect(redirect_url)

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Edit Produk',
        'button': 'Update Produk',
        'product': product,
        'page': page
    })


@login_required(login_url='/login/')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    page = request.GET.get('page') or request.POST.get('page')
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produk berhasil dihapus!')
        redirect_url = reverse('dashboard_products')
        if page:
            redirect_url += f'?page={page}'
        return redirect(redirect_url)

    return render(request, 'dashboard/product_confirm_delete.html', {
        'product': product,
        'page': page
    })


# ───────────── CRITERIA CRUD ─────────────
@login_required(login_url='/login/')
def dashboard_criteria(request):
    criteria = Criteria.objects.all()
    total_weight = sum(c.weight for c in criteria)
    return render(request, 'dashboard/criteria.html', {
        'criteria': criteria,
        'total_weight': round(total_weight, 2)
    })


@login_required(login_url='/login/')
def criteria_add(request):
    form = CriteriaForm()
    if request.method == 'POST':
        form = CriteriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kriteria berhasil ditambahkan!')
            return redirect('dashboard_criteria')

    return render(request, 'dashboard/criteria_form.html', {
        'form': form,
        'title': 'Tambah Kriteria SAW',
        'button': 'Simpan Kriteria'
    })


@login_required(login_url='/login/')
def criteria_edit(request, pk):
    criteria = get_object_or_404(Criteria, pk=pk)
    form = CriteriaForm(instance=criteria)

    if request.method == 'POST':
        form = CriteriaForm(request.POST, instance=criteria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kriteria berhasil diupdate!')
            return redirect('dashboard_criteria')

    return render(request, 'dashboard/criteria_form.html', {
        'form': form,
        'title': 'Edit Kriteria',
        'button': 'Update Kriteria'
    })


@login_required(login_url='/login/')
def criteria_delete(request, pk):
    criteria = get_object_or_404(Criteria, pk=pk)
    if request.method == 'POST':
        criteria.delete()
        messages.success(request, 'Kriteria berhasil dihapus!')
        return redirect('dashboard_criteria')

    return render(request, 'dashboard/criteria_confirm_delete.html', {
        'criteria': criteria
    })


# ───────────── PRODUCT VALUE CRUD ─────────────
@login_required(login_url='/login/')
def dashboard_values(request):
    from recommendation.saw import saw_recommendation

    categories = Category.objects.all()
    selected_category = request.GET.get('category', '')

    # 1. Panggil SAW tanpa filter budget aneh-aneh dari teman Abang
    # Agar 10 besar ranking global muncul semua!
    rankings = saw_recommendation(category=selected_category)

    # 2. Ambil nilai RAM/Baterai aslinya dari database (opsional jika dibutuhkan nanti)
    for r in rankings:
        values = ProductValue.objects.filter(
            product=r['product']
        ).select_related('criteria')
        r['values'] = {v.criteria.name: v.value for v in values}

    products = Product.objects.all()

    return render(request, 'dashboard/values.html', {
        'rankings': rankings,
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })


@login_required(login_url='/login/')
def value_add(request):
    form = ProductValueForm()
    if request.method == 'POST':
        form = ProductValueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nilai berhasil ditambahkan!')
            return redirect('dashboard_values')

    return render(request, 'dashboard/value_form.html', {
        'form': form,
        'title': 'Tambah Nilai Produk',
        'button': 'Simpan Nilai'
    })


@login_required(login_url='/login/')
def value_edit(request, pk):
    value = get_object_or_404(ProductValue, pk=pk)
    form = ProductValueForm(instance=value)

    if request.method == 'POST':
        form = ProductValueForm(request.POST, instance=value)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nilai berhasil diupdate!')
            return redirect('dashboard_values')

    return render(request, 'dashboard/value_form.html', {
        'form': form,
        'title': 'Edit Nilai Produk',
        'button': 'Update Nilai'
    })


@login_required(login_url='/login/')
def value_delete(request, pk):
    value = get_object_or_404(ProductValue, pk=pk)
    if request.method == 'POST':
        value.delete()
        messages.success(request, 'Nilai berhasil dihapus!')
        return redirect('dashboard_values')

    return render(request, 'dashboard/value_confirm_delete.html', {
        'value': value
    })