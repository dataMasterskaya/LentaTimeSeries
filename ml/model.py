import json
import logging
import numpy as np


m_logger = logging.getLogger(__name__)
m_logger.setLevel(logging.DEBUG)
handler_m = logging.StreamHandler()
formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler_m.setFormatter(formatter_m)
m_logger.addHandler(handler_m)


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