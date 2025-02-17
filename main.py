import paho.mqtt.client as mqtt
import json
import requests
# Configuración del broker
BROKER_URL = "ae1dd77d.ala.us-east-1.emqxsl.com"
BROKER_PORT = 8883
USERNAME = "paltas_sn"
PASSWORD = "ctucl2021@"
TOPIC = "paltas_sn/commands"


query_commands = ['generate_normal_pass','test_lock','test_arrow']

def api_query(param):
    url = "http://localhost:5000/api/mecanism"
    payload = {"operation": param}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)  # Usa `json=payload` en lugar de `data`
    print(response.text)

#aqui abajo ira toda la logica para ejecutar una funcion
def on_message(client, userdata, message):
    data_received = message.payload.decode()
    try:
        data_dict = json.loads(data_received)  # Convertir string JSON a diccionario
        command = str(data_dict.get('command')) # Obtener el valor de 'command'
        param = data_dict.get('param')  # Obtener el valor de 'param' por si se ocupa en algun punto
        print(command)
        if command in query_commands:
            api_query(command)
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
