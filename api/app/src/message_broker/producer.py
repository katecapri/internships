import os
import pika


def send_into_email_queue(email_info):
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue='email')
    channel.basic_publish(exchange='',
                          routing_key='email',
                          body=email_info)
    connection.close()


def send_into_request_verify_queue(request_id):
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue='request_verify')
    channel.basic_publish(exchange='',
                          routing_key='request_verify',
                          body=request_id)
    connection.close()


def send_into_points_queue(points_event_info):
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue='points')
    channel.basic_publish(exchange='',
                          routing_key='points',
                          body=points_event_info)
    connection.close()


def send_into_timesheet_queue(generate_timesheet_data):
    credentials = pika.PlainCredentials(os.getenv("RABBITMQ_DEFAULT_USER"),
                                        os.getenv("RABBITMQ_DEFAULT_PASS"))

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.getenv("RABBITMQ_HOST"),
                                  int(os.getenv("RABBITMQ_PORT")),
                                  '/', credentials)
    )

    channel = connection.channel()
    channel.queue_declare(queue='timesheet')
    channel.basic_publish(exchange='',
                          routing_key='timesheet',
                          body=generate_timesheet_data)
    connection.close()
