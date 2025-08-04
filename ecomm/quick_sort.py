def quicksort_products(products, key_func, reverse=False):
    if len(products) <= 1:
        return products
    pivot = products[len(products) // 2]
    pivot_key = key_func(pivot)

    left = [x for x in products if key_func(x) < pivot_key]
    middle = [x for x in products if key_func(x) == pivot_key]
    right = [x for x in products if key_func(x) > pivot_key]

    if reverse:
        return quicksort_products(right, key_func, reverse) + middle + quicksort_products(left, key_func, reverse)
    else:
        return quicksort_products(left, key_func, reverse) + middle + quicksort_products(right, key_func, reverse)
