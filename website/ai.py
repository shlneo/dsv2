# Импорт необходимых модулей
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Конфигурация модели
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Инициализация модели
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Отвечай на вопросы"
)

def start_chat():
    """Функция для начала нового чата."""
    return model.start_chat(history=[])

def send_message(chat_session, message):
    """Функция отправки сообщения в чат с моделью и получения ответа."""
    if not chat_session:
        chat_session = start_chat()
    
    response = chat_session.send_message(message)
    return response.text.strip()

# Пример использования
if __name__ == "__main__":
    chat = start_chat()
    while True:
        user_input = input("Вы: ")
        if user_input.lower() in ["выход", "exit", "quit"]:
            print("Чат завершен.")
            break
        response = send_message(chat, user_input)
        print("Бот:", response)
