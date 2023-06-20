# Инструменты для аннотации и визуализации данных.
Файлы с заданием №1 находятся в папке `sentiment`
- `ray_serve_api.ipynb` - пример `api` на `ray-serve`
- `fastapi_api` - реализация api на `FastAPI`
- `gradio_interface.py` - реализация интерфейса на `gradio` с использованием api на `FastAPI`
- `gradio_on_ray.py` - запуск `gradio` с помощью `ray-serve`

Файлы с заданием №2 находятся в папке `dialogs`
- `annotations.py` - реализация интерфейса аннотации диалогов на `streamlit`
- `dialogs_gradio.py` - визуализация распределения эмоций в диалогах в зависимости от жанра фильма на `gradio`
- `dialogs_streamlit.py` - интерфейс для просмотра распределения эмоций реплик из диалогов фильмов на `streamlit`
- `emotions_mapping.ipynb` - разметка реплик в эмоции с помощью модели из `huggingface`
- `data_processing.ipynb` - предварительная обработка данных для разметки и выполнения задания
