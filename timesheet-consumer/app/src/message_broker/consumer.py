import asyncio
import logging
import os
import pika
import json
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - [%(levelname)s]: %(message)s')


async def receive_into_timesheet_queue():
    logging.info(" [x] Consumer started")
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue='timesheet')

    def callback(ch, method, properties, body):
        try:
            body = json.loads(body)
            logging.info(f" [x] Received a message from the timesheet queue: {body}")
            response = requests.post(
                f"{os.getenv('TIMESHEET_URL')}/api/v1/timesheet/",
                json=body
            )
            if response.status_code in (200, 201):
                ch.basic_ack(delivery_tag=method.delivery_tag)
                logging.info(" [x] Message processing completed")
            else:
                logging.info(" [Х] No positive response was received from request")
        except Exception as e:
            logging.error(e, exc_info=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='timesheet',
                          on_message_callback=callback,
                          auto_ack=False)

    channel.start_consuming()


if __name__ == '__main__':
    asyncio.run(receive_into_timesheet_queue())
