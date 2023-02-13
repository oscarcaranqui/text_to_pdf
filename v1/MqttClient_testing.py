import paho.mqtt.client as mqtt
import time

class MobilePhone:
    def __init__(self, client_name, subscribe_topic, publish_topic):
        self.nombre_cliente = client_name
        self.topic_subscribe = subscribe_topic
        self.topic_publish = publish_topic
        self.client = mqtt.Client(client_id=self.nombre_cliente, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message


    # Callback for when the MQTT client connects
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado con éxito al broker.")
            client.subscribe(self.topic_subscribe)
        else:
            print("Fallo al conectar con el broker. Código de salida:", rc)

    # Callback for when the MQTT client disconnects
    def on_disconnect(self, client, userdata, rc):
        # Reconectar automáticamente después de 5 segundos si se produce una desconexión inesperada
        if rc != 0:
            time.sleep(5)
            print("Inesperada desconexion del broker. Código de salida:", rc)

    # Callback for when a message arrives to a subscribed topic
    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8").replace("\\n", "\n")
        print("Received message: " + payload)

    def send_request(self, publish_message):
        self.client.publish(self.topic_publish, publish_message, retain=False)
        print("Sent message:\n" + publish_message)

    def run(self, broker, port):
        self.client.connect(broker, port, 60)
        # Start loop to receive messages
        self.client.loop_start()

