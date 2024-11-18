import asyncio
import logging
import os
import pika
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s]: %(message)s')


async def receive_into_request_verify_queue():
    logging.info(" [x] Consumer started")
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='request_verify')

    def callback(ch, method, properties, body):
        try:
            body = body.decode()
            logging.info(f" [x] Received a message from the request_verify queue")
            headers = {"API_CONSUMER_KEY": os.getenv("API_CONSUMER_KEY")}

            response = requests.post(
                f"{os.getenv('API_URL')}/api/v1/request/{body}/verify/",
                headers=headers
            )
            if response.status_code == 201 or response.status_code == 200:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logging.info(" [x] Message processing completed")
            else:
                logging.info(" [Х] No positive response was received from request.")
        except Exception as e:
            logging.error(e, exc_info=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='request_verify',
                          on_message_callback=callback,
                          auto_ack=False)

    channel.start_consuming()


if __name__ == '__main__':
    asyncio.run(receive_into_request_verify_queue())
