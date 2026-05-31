# GANTI ALAMATNYA KE PRODUCTS (Kamar yang benar!)
from products.models import Product, Criteria, ProductValue

def saw_recommendation(user_weights=None, category=None):
    # 1. Ambil semua produk terlebih dahulu
    products = Product.objects.all()
    
    # 2. Filter Kategori (Jika user memilih dropdown)
    if category:
        products = products.filter(category_id=category)
        
    # 3. FITUR CERDAS: Filter Budget
    if user_weights and 'harga' in user_weights:
        budget_maksimal = user_weights['harga']
        products = products.filter(price__lte=budget_maksimal)

    criteria = Criteria.objects.all()
    
    # Gembok pengaman: Jika produk/kriteria kosong, hentikan
    if not products.exists() or not criteria.exists():
        return []

    # 4. Ambil data Nilai
    product_ids = products.values_list('id', flat=True)
    all_values = ProductValue.objects.filter(product_id__in=product_ids).select_related('criteria')
    data_map = {(pv.product_id, pv.criteria_id): pv.value for pv in all_values}
    
    # 5. Cari nilai Maximum (Benefit) dan Minimum (Cost)
    stats = {}
    for crit in criteria:
        vals = [pv.value for pv in all_values if pv.criteria_id == crit.id]
        if vals: 
            stats[crit.id] = {'max': max(vals), 'min': min(vals)}

    result = []
    
    # 6. Total bobot
    total_weight = sum([c.weight for c in criteria])

    # 7. Proses Perhitungan Inti SAW
    for product in products:
        score = 0
        for crit in criteria:
            val = data_map.get((product.id, crit.id), 0)
            weight = crit.weight 
            stat = stats.get(crit.id)
            
            if stat and val != 0:
                if crit.type == 'cost':
                    norm = stat['min'] / val if val != 0 else 0
                else:
                    norm = val / stat['max'] if stat['max'] != 0 else 0
                
                score += norm * weight

        final_score = (score / total_weight) * 100 if total_weight > 0 else 0
        result.append({"product": product, "score": round(final_score, 1)})

    # 8. Urutkan dari tertinggi dan ambil 10 BESAR
    sorted_result = sorted(result, key=lambda x: x['score'], reverse=True)
    return sorted_result[:10]