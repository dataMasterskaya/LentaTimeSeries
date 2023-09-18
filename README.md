# lenta_backend

## Структура репозитория
/backend
- app.py - приложение с хэндлерами
- categories.json - имитация базы данных с категориями товаров
- sales.json - имитация базы данных по продажам
- stores.json - имитация базы данных с магазинами
- forecast_archive.json - файл для записи предсказаний

/ml
- model.py - имитация модели машинного обучения

**Сборка**
```bash
docker build --tag timeseries .
```
**Запуск**
```bash
docker run --rm -it -p 8010:8000 --name lenta timeseries
```

**После этого сервис работает по адресу**
```bash
localhost:8010/
```
