import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from getpass import getpass

from langchain_gigachat.chat_models.gigachat import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage

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


def check_task(task_name: str) -> str:
    messages = [
        SystemMessage(content="""Ты - эксперт по проверки наименований задач на соответствие требованиям SMART и DoD.
                                Тебе будет дано название задачи [TASK] для проверки.
                                Ты должен дать оценку в строгом формате: Наименование КР не сформулировано в виде SMART/DOD - если задача не соответствует требованиям, ОК - если соответствует.
                                
                                Примеры:
                                [TASK] Завершены работы по адаптации каналов коммуникаций с банком на РЖЯ. Твой ответ: ОК.
                                [TASK] Работа с оттоком. Разработаны пакеты услуг для сохранения клиентов в банке. Твой ответ: ОК.
                                [TASK] Совместный кредитный счет. Твой ответ: Наименование КР не сформулировано в виде SMART/DOD.
                                [TASK] Развитие и поддержание HR бренда Трайба Лояльность. Твой ответ: Наименование КР не сформулировано в виде SMART/DOD.

        """),
        HumanMessage(content=f"[TASK] {task_name}"),
    ]
    response = model.invoke(messages)
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