import pika
import time
import json

REQUEST_QUEUE = 'model_training_request'
RESPONSE_QUEUE = 'model_training_response'


def train_model(params):
    print(f"Starting model training with parameters: {params}")
    time.sleep(5)  # 模拟训练过程
    return {"status": "success", "message": "Model training completed"}


def on_message(ch, method, properties, body):
    print(f" [x] Received: {body.decode()}")
    # params = json.loads(body)
    result = train_model("params")

    # 模型训练完成后，将结果发送到 RESPONSE_QUEUE
    credentials = pika.PlainCredentials('peppa', 'xpy3464..')  # mq用户名和密码
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='47.120.25.129', port=5672, virtual_host='/', credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=RESPONSE_QUEUE)
    channel.basic_publish(exchange='', routing_key=RESPONSE_QUEUE, body=json.dumps(result))
    print(f" [x] Sent: {result}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

credentials = pika.PlainCredentials('peppa', 'xpy3464..')  # mq用户名和密码
connection = pika.BlockingConnection(pika.ConnectionParameters(host = '47.120.25.129',port = 5672,virtual_host = '/',credentials = credentials))
channel = connection.channel()
channel.queue_declare(queue=REQUEST_QUEUE)
channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=on_message)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
