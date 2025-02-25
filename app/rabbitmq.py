import pika, json, asyncio
from app.websocket import websocket_manager
from app.config import RABBITMQ_URL
import ssl
import asyncio
import json

def callback(ch, method, properties, body):
    try:
        print(f"Received message: {body}")
        message = json.loads(body)
        user_id = message.get("user_id")
        order_status = message.get("order").get("status")

        if user_id and order_status:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(
                websocket_manager.send_order_update(user_id, f"order status updated: {order_status}")
            )
            loop.close()
    except Exception as e:
        print(f"Error processing message: {e}")


def consume_order_updates():
    params = pika.URLParameters(RABBITMQ_URL)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  

    params.ssl_options = pika.SSLOptions(context)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="user_validation_queue")
    channel.basic_consume(queue="user_validation_queue", on_message_callback=callback, auto_ack=True)

    print("Waiting for order updates...")
    channel.start_consuming()
