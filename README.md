
DeltoBot es un bot de Telegram diseñado para proporcionar información meteorológica, contar interacciones, analizar sentimientos de conversaciones y recomendar actividades basadas en la ubicación del usuario. Este bot utiliza la API de OpenWeatherMap para obtener datos meteorológicos y la API de OpenAI para análisis de sentimientos y generación de contenido.

Funcionalidades
Parte 1: El comienzo
Menú Principal:

Opciones:
¡Quiero saber el clima!
¡Quiero contar!
Funcionalidad del Clima:

El bot responde a la solicitud del clima en una ciudad específica utilizando la API de OpenWeatherMap.
La respuesta incluye la temperatura actual, condiciones climáticas y una recomendación basada en el clima (por ejemplo, "Lleva un paraguas" si está lloviendo).
Contador:

Implementa un contador que se incrementa en uno cada vez que el usuario interactúa con esta opción.
El contador es persistente y se mantiene incluso si el bot se reinicia.
El contador es único por usuario.
Parte 2: Integración con OpenAI
Analizar Comentario:

Opción en el menú del bot que permite enviar la conversación del usuario con el Bot a OpenAI.
Utiliza la API de OpenAI para analizar el sentimiento de la conversación.
Clasifica el sentimiento como positivo, negativo o neutral y proporciona una breve explicación.
Generación de Respuesta Inteligente:

Cuando el usuario consulta el clima, el bot ofrece una respuesta adicional generada por OpenAI para mejorar la experiencia del usuario. Por ejemplo, después de proporcionar el clima, el bot puede ofrecer consejos adicionales o información interesante sobre la ciudad.
Parte 3: Creatividad
Funcionalidad Libre:
Recomendar Actividades: El bot puede recomendar actividades y lugares de interés en una ciudad específica. Esta funcionalidad mejora la experiencia del usuario al proporcionar información adicional sobre su destino.
Explicación: Decidí agregar esta funcionalidad porque enriquece la experiencia del usuario al proporcionarle no solo el clima, sino también sugerencias sobre qué hacer en la ciudad que está consultando. Esto puede ser especialmente útil para turistas o personas que buscan explorar nuevas áreas.
Instalación
Clona este repositorio:

bash
Copy code
git clone https://github.com/tu-usuario/DeltoBot.git
Navega al directorio del proyecto:

bash
Copy code
cd DeltoBot
Crea y activa un entorno virtual:

bash
Copy code
python -m venv delto_env
source delto_env/bin/activate  # En Windows: delto_env\Scripts\activate
Instala las dependencias:

bash
Copy code
pip install -r requirements.txt
Crea un archivo .env en el directorio raíz del proyecto y agrega tus claves de API:

env
Copy code
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
OPENWEATHERMAP_API_KEY=your-openweathermap-api-key
OPENAI_API_KEY=your-openai-api-key
Uso
Inicia el bot:

bash
Copy code
python bot.py
En Telegram, busca tu bot usando su nombre de usuario y comienza una conversación con el comando /start.

Dependencias
python-dotenv
requests
python-telegram-bot
openai# DeltoBot
