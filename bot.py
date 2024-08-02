from dotenv import load_dotenv
import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
)
from counter import increment_counter  
from openai import OpenAI

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)


def get_weather(city: str) -> str:
    api_key = OPENWEATHERMAP_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return f"La temperatura en {city} es {temp}°C con {description}. " + \
               ("Lleva un paraguas." if "rain" in description else "Disfruta del buen tiempo.")
    else:
        return "No se pudo obtener el clima. Por favor, verifica el nombre de la ciudad."


def analyze_sentiment(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un analizador de sentimientos."},
                {"role": "user", "content": f"Analiza el sentimiento del siguiente texto y clasifícalo como positivo, negativo o neutral:\n\n{text}"}
            ],
            max_tokens=60
        )
        sentiment = response.choices[0].message['content'].strip()
        return sentiment
    except Exception as e:
        return f"Error al analizar el sentimiento: {e}"


async def weather(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    if not city:
        await update.message.reply_text('Por favor, proporciona el nombre de la ciudad.')
        return
    weather_info = get_weather(city)
    additional_info = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente de clima."},
            {"role": "user", "content": f"Después de dar el clima en {city}, proporciona información interesante sobre la ciudad."}
        ],
        max_tokens=60
    ).choices[0].message['content'].strip()
    await update.message.reply_text(f"{weather_info}\n\n{additional_info}")


async def recommend_activities(update: Update, context: CallbackContext) -> None:
    city = ' '.join(context.args)
    if not city:
        await update.message.reply_text('Por favor, proporciona el nombre de la ciudad.')
        return
    recommendations = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente de viajes."},
            {"role": "user", "content": f"Recomienda algunas actividades y lugares de interés en {city}."}
        ],
        max_tokens=150
    ).choices[0].message['content'].strip()
    await update.message.reply_text(f"Actividades recomendadas en {city}:\n\n{recommendations}")


async def analyze_conversation(update: Update, context: CallbackContext) -> None:
    user_conversation = "\n".join([msg.text for msg in context.user_data.get('messages', [])])
    sentiment = analyze_sentiment(user_conversation)
    await update.message.reply_text(f"El sentimiento de tu conversación es: {sentiment}")


async def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [
        ['¡Quiero saber el clima!', '¡Quiero contar!'],
        ['¡Analizar conversación!', '¡Recomendar actividades!']
    ]
    await update.message.reply_text(
        'Hola! Soy DeltoBot. ¿Qué quieres hacer?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )


async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    user_id = update.message.from_user.id

    if 'messages' not in context.user_data:
        context.user_data['messages'] = []

    context.user_data['messages'].append(update.message)

    if text == '¡Quiero saber el clima!':
        await update.message.reply_text('Por favor, envía el nombre de la ciudad usando el comando /clima seguido del nombre.')
    elif text == '¡Quiero contar!':
        count = increment_counter(user_id)
        await update.message.reply_text(f'Has interactuado {count} veces.')
    elif text == '¡Analizar conversación!':
        await analyze_conversation(update, context)
    elif text == '¡Recomendar actividades!':
        await update.message.reply_text('Por favor, envía el nombre de la ciudad usando el comando /recomendar seguido del nombre de tu ciudad.')
    else:
        await update.message.reply_text('Por favor, elige una opción del menú.')


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clima", weather))
    application.add_handler(CommandHandler("recomendar", recommend_activities))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.run_polling()


if __name__ == '__main__':
    main()
