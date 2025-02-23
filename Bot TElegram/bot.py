import telebot
from PIL import Image
from io import BytesIO 
from logic import leer_productos, añadir_producto
import base64
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = 'TU token'
bot = telebot.TeleBot(TOKEN)
bot1 = telebot.TeleBot('Token')
productos = leer_productos()
chat_id= 'tu chatID'

# Variable para controlar el estado de repetición
repeat_mode = False

# Comando de inicio
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, '¡Hola! Soy tu bot')

# Comando para activar la repetición
@bot.message_handler(commands=['repetir'])
def activate_repeat(message):
    global repeat_mode
    repeat_mode = True
    bot.reply_to(message, 'Modo repetir activado. Escribe "/salir" para desactivarlo.')

# Comando para desactivar la repetición
@bot.message_handler(commands=['salir'])
def deactivate_repeat(message):
    global repeat_mode
    repeat_mode = False
    bot.reply_to(message, 'Modo repetir desactivado.')

# Comando para enviar una imagen
@bot.message_handler(commands=['qaf'])
def send_image(message):
    # Abre la imagen
    image = Image.open('Foto LilosSHOP.jpg')
    image = image.convert('RGB')
    
    # Guarda la imagen en un objeto BytesIO
    image_byte_array = BytesIO()
    image.save(image_byte_array, format='JPEG')
    
    # Mueve el puntero al inicio del archivo BytesIO
    image_byte_array.seek(0)
    
    # Envía la foto
    bot.send_photo(message.chat.id, image_byte_array, caption='Nos dedicamos a la venta principalmente de cosas para bebes y para la mamis. Somos de Alamar. Contamos con mensajería.')
# Función para repetir mensajes
@bot.message_handler(func=lambda message: repeat_mode)
def echo_message(message):
    if repeat_mode:
        bot.reply_to(message, message.text)

@bot.message_handler(commands=['productos'])
def enviar_producto(message):
    # Leer productos desde el archivo JSON
    productos = leer_productos()
    
    # Iterar sobre los productos y enviar la información y la foto
    for producto in productos:
        nombre = producto['nombre']
        descripcion = producto['precio']
        foto_base64 = producto['foto']
        
        # Convertir la cadena base64 de la imagen a un objeto BytesIO
        foto_bytes = base64.b64decode(foto_base64)
        image_byte_array = BytesIO(foto_bytes)
        
        # Crear el teclado inline con un botón
        keyboard = InlineKeyboardMarkup()
        order_button = InlineKeyboardButton(text='Enviar orden', callback_data=f'orden_{nombre}')
        keyboard.add(order_button)
        
        # Enviar información del producto junto con la foto y el teclado inline
        caption = f"Nombre del producto: {nombre}\nPrecio: {descripcion}"
        bot.send_photo(message.chat.id, image_byte_array, caption=caption, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('orden_'))
def handle_order(call):
    nombre_producto = call.data.split('_')[1]
    mensaje_respuesta = f"{call.from_user.first_name} ha enviado una orden para: {nombre_producto}"
    
    contact_button = InlineKeyboardButton(text="Contactar al Usuario", url=f"tg://user?id={call.from_user.id}")
    reply_markup = InlineKeyboardMarkup([[contact_button]])
    
    # Enviar el mensaje de respuesta al chat con el botón
    bot1.send_message(chat_id, mensaje_respuesta, reply_markup=reply_markup)

def start_bot():
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(2)  # Esperar 2 segundos antes de reintentar

if __name__ == '__main__':
    start_bot()





