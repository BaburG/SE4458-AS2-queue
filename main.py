from fastapi import FastAPI, Form, HTTPException
from typing import Annotated
import aio_pika
from contextlib import asynccontextmanager
import asyncio
import json

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global channel, connection
    print("Starting FastAPI service")
    
    # Connect to RabbitMQ server
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    print("Connected to RabbitMQ service")
    
    channel = await connection.channel()
    await channel.declare_queue("payment_queue", durable=True)
    print("Created payment queue")
    await channel.declare_queue("notification_queue", durable=True)
    print("Created notification queue")

    asyncio.create_task(process_payment())
    asyncio.create_task(notify())

    yield  # The app runs here

    await connection.close()
    print("Closed RabbitMQ connection")
    print("Shutting down FastAPI service")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/make-payment")
async def make_payment(
    user: Annotated[str, Form()],
    paymentType: Annotated[str, Form()],
    cardNo: Annotated[str, Form()]
):
    if not user or not paymentType or not cardNo:
        raise HTTPException(
            status_code=415, detail="EMPTY FIELD"
        )
    
    message = {
        "user": user,
        "paymentType": paymentType,
        "cardNo": cardNo
    }
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key="payment_queue"
    )
    print("Payment request sent")
    return {"status": "Payment request sent"}


async def process_payment():
    """Consume messages from payment_queue and produce for notification_queue."""
    print("Starting process_payment consumer")
    async with connection.channel() as channel:
        payment_queue = await channel.get_queue("payment_queue")
        notification_exchange = channel.default_exchange

        async for message in payment_queue:
            
            async with message.process():
                await asyncio.sleep(0.05)
                # Process payment message
                payment_data = json.loads(message.body.decode())
                print(f"Processing payment for user: {payment_data['user']}")
                
                # Send notification
                notification_message = {
                    "user": payment_data["user"],
                    "status": "Payment received"
                }
                await notification_exchange.publish(
                    aio_pika.Message(body=json.dumps(notification_message).encode()),
                    routing_key="notification_queue"
                )
                print("Notification message sent")


async def notify():
    """Consume messages from notification_queue and print them."""
    print("Starting notify consumer")
    async with connection.channel() as channel:
        
        notification_queue = await channel.get_queue("notification_queue")

        async for message in notification_queue:
            async with message.process():
                await asyncio.sleep(0.05)
                # Print notification message
                notification_data = json.loads(message.body.decode())
                print(f"Notification received: {notification_data}")

