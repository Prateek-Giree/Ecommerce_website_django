def linear_search_partial(products, target):
    matches = []
    for product in products:
        if target.lower() in product.name.lower():
            matches.append(product)
    return matches
