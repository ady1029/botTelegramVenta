import json
import os
from PIL import Image
from io import BytesIO
import base64

# Verificar si el archivo existe y tiene contenido
def inicializar_archivo_json():
    if not os.path.exists('productos.json') or os.path.getsize('productos.json') == 0:
        with open('productos.json', 'w') as file:
            file.write('[]')

# Leer productos desde un archivo JSON
def leer_productos():
    inicializar_archivo_json()
    with open('productos.json', 'r') as file:
        return json.load(file)

# Guardar productos en un archivo JSON
def guardar_productos(productos):
    with open('productos.json', 'w') as file:
        json.dump(productos, file, indent=4)

# Añadir un nuevo producto
def añadir_producto(nombre, foto, precio):
    productos = leer_productos()
    # Convertir la imagen a bytes y codificar en base64
    with Image.open(foto) as imagen:
        image_byte_array = BytesIO()
        imagen.convert('RGB').save(image_byte_array, format='JPEG')
        foto_bytes = base64.b64encode(image_byte_array.getvalue()).decode('utf-8')
    productos.append({"nombre": nombre, "foto": foto_bytes, "precio": precio})
    guardar_productos(productos)

def borrar_producto(nombre):
    productos = leer_productos()
    productos = [producto for producto in productos if producto["nombre"] != nombre]
    guardar_productos(productos)

def contar_productos():
    productos = leer_productos()
    return len(productos)

# Inicializar el archivo JSON
inicializar_archivo_json()
