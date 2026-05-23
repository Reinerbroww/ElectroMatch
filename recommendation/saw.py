from products.models import Product, Criteria, ProductValue

def normalize(values, is_cost=False):
    if is_cost:
        min_val = min(values)
        return [min_val / v if v != 0 else 0 for v in values]
    else:
        max_val = max(values)
        return [v / max_val if max_val != 0 else 0 for v in values]


def saw_recommendation():
    products = Product.objects.all()
    criteria = Criteria.objects.all()

    result = []

    for product in products:
        score = 0

        for crit in criteria:
            try:
                pv = ProductValue.objects.get(product=product, criteria=crit)
                value = pv.value

                # normalisasi cost/benefit
                if crit.type == 'cost':
                    all_values = [
                        ProductValue.objects.get(product=p, criteria=crit).value
                        for p in products
                    ]
                    normalized = min(all_values) / value if value != 0 else 0
                else:
                    all_values = [
                        ProductValue.objects.get(product=p, criteria=crit).value
                        for p in products
                    ]
                    normalized = value / max(all_values) if max(all_values) != 0 else 0

                score += normalized * crit.weight

            except ProductValue.DoesNotExist:
                continue

        result.append({
            "product": product,
            "score": round(score, 3)
        })

    # urutkan dari terbesar
    result = sorted(result, key=lambda x: x['score'], reverse=True)

    return result