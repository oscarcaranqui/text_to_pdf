import pika


def consume_queue(callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='test', durable=True)
    channel.basic_consume(queue='test', on_message_callback=callback)

    try:
        print("Waiting messages.....")
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)











