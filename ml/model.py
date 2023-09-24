def forecast(sales: dict, item_info: dict, store_info: dict) -> list:
    """
    Функция для предсказания продажЖ
    :params sales: исторические данные по продажам
    :params item_info: характеристики товара
    :params store_info: характеристики магазина

    """
    sales = [el["sales_units"] for el in sales]
    mean_sale = sum(sales) / len(sales)
    return [mean_sale] * 5