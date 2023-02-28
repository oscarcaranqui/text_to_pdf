from v1.layout import DOCUMENT
from dataclass_wizard import JSONWizard
from v1.consumer import consume_queue
from dataclasses import dataclass
import multiprocessing


@dataclass
class Sender(JSONWizard):
    formattedName: str


@dataclass
class IncomingMessage(JSONWizard):
    sender: Sender
    payload: str
    number: str
    chatId: str

    @staticmethod
    def get_info(body: bytes):
        result = IncomingMessage.from_json(body.decode())
        contact_name = result.sender.formattedName
        payload = result.payload
        number = result.number
        chat_id = result.chatId
        return contact_name, payload, number, chat_id


@dataclass
class OutgoingMessage(JSONWizard):
    sender: str
    payload: str
    number: str

    @staticmethod
    def set_info(contact_name, response_message, number):
        message = OutgoingMessage(contact_name, response_message, number).to_json()
        return message


class app:
    def __init__(self):
        self.message_handler()

    @staticmethod
    def send_message(contact_name: str, response_message: str, number: str, channel):
        data = OutgoingMessage.set_info(contact_name, response_message, number)
        channel.basic_publish(exchange='', routing_key='responses', body=data)
        print(f" [x] Sent '{response_message}'")

    @staticmethod
    def message_handler():
        def callback(ch, method, properties, body):
            contact_name, payload, number, chat_id = IncomingMessage.get_info(body)
            result = DOCUMENT().write_pdf(payload)
            app.send_message(contact_name, result, number, ch)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        consumer = multiprocessing.Process(target=consume_queue(callback))
        consumer.start()


if __name__ == '__main__':
    app()

