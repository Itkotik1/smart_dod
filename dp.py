import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
load_dotenv()

OPEN_ROUTER_KEY=os.getenv("OPEN_ROUTER_KEY")

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OPEN_ROUTER_KEY,
)
def check_task(task_name: str) -> str:
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
      },
      extra_body={},
      model="deepseek/deepseek-r1-0528-qwen3-8b:free",
      messages=[
        {
            "role": "system",
            "content": """
                Ты - эксперт по проверки наименований задач на соответствие требованиям SMART и DoD.
                Тебе будет дано название задачи [TASK] для проверки.
                Ты должен дать оценку в строгом формате: Наименование КР не сформулировано в виде SMART/DOD - если задача не соответствует требованиям, ОК - если соответствует.
                                    
                Примеры:
                [TASK] Завершены работы по адаптации каналов коммуникаций с банком на РЖЯ. Твой ответ: ОК.
                [TASK] Работа с оттоком. Разработаны пакеты услуг для сохранения клиентов в банке. Твой ответ: ОК.
                [TASK] Совместный кредитный счет. Твой ответ: Наименование КР не сформулировано в виде SMART/DOD.
                [TASK] Развитие и поддержание HR бренда Трайба Лояльность. Твой ответ: Наименование КР не сформулировано в виде SMART/DOD.
            """
        },
        {
          "role": "user",
          "content": f"[TASK] {task_name}"
        }
      ]
    )
    return completion.choices[0].message.content

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

