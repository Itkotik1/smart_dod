import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from getpass import getpass

from langchain_gigachat.chat_models.gigachat import GigaChat

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Если ключ не задан — запрашиваем его у пользователя
if "GIGACHAT_CREDENTIALS" not in os.environ:
    os.environ["GIGACHAT_CREDENTIALS"] = getpass("Введите ключ авторизации GigaChat API: ")

# Инициализация модели
model = GigaChat(
    model="GigaChat-Pro",
    verify_ssl_certs=False
)

# Функция проверки задачи
def check_task(task_name: str) -> str:
    prompt = f"""
    Проверь следующую задачу на соответствие принципам SMART (Specific, Measurable, Achievable, Relevant, Time-bound) 
    и Definition of Done (DoD): "{task_name}".

    Оцени её и верни один из трёх вариантов:
    - соответствует
    - не точное соответствие
    - не соответствует
    """
    response = model.invoke(prompt)
    return response.content.strip()

# Чтение данных из Excel
input_file = "tasks.xlsx"
output_file = "tasks_with_results.xlsx"

df = pd.read_excel(input_file)

# Предполагается, что столбец с названиями задач называется "Название"
if "Название" not in df.columns:
    raise ValueError("В таблице отсутствует столбец 'Название'")

# Обработка каждой задачи
df["Результат проверки"] = df["Название"].apply(check_task)

# Сохранение результата в новый файл
df.to_excel(output_file, index=False)

print(f"Обработка завершена. Результат сохранён в {output_file}")