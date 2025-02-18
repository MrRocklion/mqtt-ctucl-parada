import paho.mqtt.client as mqtt
import json
import requests
from dotenv import load_dotenv
import os
# Corgar variables desde un archivo .env
load_dotenv()
BROKER_URL = os.getenv("BROKER_URL")
BROKER_PORT = int(os.getenv("BROKER_PORT"))
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TOPIC = os.getenv("TOPIC")


def api_query(command,path):
    url = f"http://localhost:5000/api/{path}"
    payload = {"operation": command}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)  # Usa `json=payload` en lugar de `data`
    print(response.text)

#aqui abajo ira toda la logica para ejecutar una funcion
def on_message(client, userdata, message):
    data_received = message.payload.decode()
    try:
        data_dict = json.loads(data_received)  # Convertir string JSON a diccionario
        command = str(data_dict.get('command')) # Obtener el valor de 'command'
        path = str(data_dict.get('path'))  # Obtener el valor de 'param' por si se ocupa en algun punto
        print(command)
        if command != "":
            api_query(command,path)
        else:
            pass
    except json.JSONDecodeError:
        print("Error: el mensaje recibido no es un JSON válido")

# Callback cuando se establece la conexión
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker MQTT")
        client.subscribe(TOPIC)
        print(f"Suscrito al tópico: {TOPIC}")
    else:
        print(f"Error de conexión, código: {rc}")

# Configurar el cliente MQTT
client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.tls_set()  # Habilitar TLS para MQTTs

client.on_connect = on_connect
client.on_message = on_message

# Conectarse al broker
client.connect(BROKER_URL, BROKER_PORT, 60)

# Mantener el cliente en ejecución
client.loop_forever()
