from products.models import Product, Criteria, ProductValue

def saw_recommendation(category=None, budget=None, kebutuhan=None):
    # filter produk berdasarkan kategori & budget
    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if budget:
        products = products.filter(price__lte=budget)

    criteria = Criteria.objects.all()

    if not products.exists():
        return []

    # bangun matrix nilai
    matrix = {}
    for product in products:
        matrix[product.id] = {}
        for c in criteria:
            pv = ProductValue.objects.filter(
                product=product,
                criteria=c
            ).first()
            matrix[product.id][c.id] = pv.value if pv else 0

    # normalisasi
    normalized = {}
    for c in criteria:
        values = [matrix[p.id][c.id] for p in products]

        if not any(values):
            for p in products:
                normalized.setdefault(p.id, {})[c.id] = 0
            continue

        if c.type == 'benefit':
            max_val = max(values) or 1
            for p in products:
                normalized.setdefault(p.id, {})[c.id] = matrix[p.id][c.id] / max_val
        else:  # cost
            min_val = min(v for v in values if v > 0) or 1
            for p in products:
                val = matrix[p.id][c.id]
                normalized.setdefault(p.id, {})[c.id] = min_val / val if val > 0 else 0

    # hitung skor akhir
    scores = []
    for p in products:
        score = sum(
            normalized[p.id][c.id] * c.weight
            for c in criteria
        )
        scores.append({
            "product": p,
            "score": round(score, 4)
        })

    return sorted(scores, key=lambda x: x["score"], reverse=True)