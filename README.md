# Хакатон "Предсказание временных рядом"

В этом репозитории вы найдёте пример того, как могут выглядеть API Gateway и ML сервисы, а также как организовать взаимодействие этих сервисов.

## Структура репозитория
/backend
- app.py - приложение с хэндлерами
- categories.json - имитация базы данных с категориями товаров
- sales.json - имитация базы данных по продажам
- stores.json - имитация базы данных с магазинами
- forecast_archive.json - файл для записи предсказаний

/ml
- model.py - имитация модели машинного обучения


## Полезные ссылки
- [Архитектура микросервисов](https://habr.com/ru/companies/vk/articles/320962/)
- [Основы REST](https://tproger.ru/articles/osnovy-rest-teorija-i-praktika?ysclid=lmxefuafdd378867233)
- [Введение в Postman](https://habr.com/ru/companies/kolesa/articles/351250/)
- [Курс Docker c нуля](https://karpov.courses/docker)