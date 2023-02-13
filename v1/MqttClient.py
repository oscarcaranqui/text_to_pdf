import paho.mqtt.client as mqtt
import time
from v1.layout import DOCUMENT

class MQTTClient:
    def __init__(self, client_name, subscribe_topic, publish_topic):
        self.client_name = client_name
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.client = mqtt.Client(client_id=self.client_name, clean_session=True)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

    # Callback for when the MQTT client connects
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to broker.")
            client.subscribe(self.subscribe_topic)
        else:
            print("Failed to connect to broker. Exit code:", rc)

    # Callback for when the MQTT client disconnects
    def on_disconnect(self, client, userdata, rc):
        # Automatically reconnect after 5 seconds if an unexpected disconnection occurs
        if rc != 0:
            time.sleep(5)
            print("Unexpected disconnection from broker. Exit code:", rc)

    # Callback for when a message arrives to a subscribed topic
    def on_message(self, client, userdata, message):
        payload = message.payload.decode("utf-8").replace("\\n", "\n")
        print("Received message: \n" + payload)
        result = DOCUMENT().write_pdf(payload)
        client.publish(self.publish_topic, "\n" + result, retain=False)

    def run(self, broker, port):
        self.client.connect(broker, port, 60)
        # Start loop to receive messages
        self.client.loop_forever()


