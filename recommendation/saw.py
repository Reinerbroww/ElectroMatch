from products.models import Product, Criteria, ProductValue

def saw_recommendation(user_weights=None, category=None):
    # 1. Filter produk berdasarkan kategori jika user memilih dari dropdown
    if category:
        products = Product.objects.filter(category_id=category) 
    else:
        products = Product.objects.all()
        
    criteria = Criteria.objects.all()
    
    # 2. Pre-fetch data agar query database secepat kilat (Instan)
    all_values = ProductValue.objects.select_related('product', 'criteria')
    data_map = {(pv.product_id, pv.criteria_id): pv.value for pv in all_values}
    
    # 3. Cari nilai Maximum (Benefit) dan Minimum (Cost)
    stats = {}
    for crit in criteria:
        vals = [pv.value for pv in all_values if pv.criteria_id == crit.id]
        if vals: 
            stats[crit.id] = {'max': max(vals), 'min': min(vals)}

    result = []
    
    # 4. Hitung total bobot maksimal untuk dijadikan persentase (0-100%)
    total_weight = sum([user_weights.get(c.name.lower(), c.weight) for c in criteria]) if user_weights else sum([c.weight for c in criteria])

    # 5. Proses Perhitungan SAW
    for product in products:
        score = 0
        for crit in criteria:
            val = data_map.get((product.id, crit.id), 0)
            
            # Ambil bobot dari slider
            weight = user_weights.get(crit.name.lower(), crit.weight) if user_weights else crit.weight
            
            stat = stats.get(crit.id)
            if stat:
                # Normalisasi Matriks
                if crit.type == 'cost':
                    norm = stat['min'] / val if val != 0 else 0
                else:
                    norm = val / stat['max'] if stat['max'] != 0 else 0
                
                # Kalikan dengan bobot
                score += norm * weight

        # Ubah skor ke bentuk persentase yang mudah dibaca
        final_score = (score / total_weight) * 100 if total_weight > 0 else 0
        result.append({"product": product, "score": round(final_score, 1)})

    # Urutkan dari produk dengan skor tertinggi (Terbaik)
    return sorted(result, key=lambda x: x['score'], reverse=True)