import pika

# Step 1: Set up connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Step 2: Declare a dedicated RPC queue and exchange
rpc_queue = 'rpc_queue'
exchange = 'rpc_exchange'
channel.exchange_declare(exchange=exchange, exchange_type='direct')
channel.queue_declare(queue=rpc_queue)

def on_request(ch, method, props, body):
    # Process the request and generate the response
    request_message = body.decode()
    response_message = "Response to '{}'".format(request_message)

    # Send the response back to the requester
    channel.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response_message
    )

    # Acknowledge the request message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Step 3: Start consuming from the RPC queue
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rpc_queue, on_message_callback=on_request)

# Start consuming
channel.start_consuming()
