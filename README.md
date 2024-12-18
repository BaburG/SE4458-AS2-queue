# Payment Processing Service

This project demonstrates a basic **payment processing service** built with **FastAPI** and **RabbitMQ**. The service includes endpoints to submit payment information and processes the requests asynchronously. The processed requests are routed to a notification queue to notify users.

## Features
- Accept payment information via a POST endpoint.
- Process payment asynchronously using RabbitMQ.
- Send payment notifications to a separate queue for further processing.

---

## Design Overview

1. **FastAPI Application**:
   - Accepts payment requests.
   - Publishes the request to the `payment_queue`.

2. **RabbitMQ**:
   - Acts as the message broker.
   - Two queues:
     - `payment_queue`: Receives payment requests.
     - `notification_queue`: Receives notifications after payments are processed.

3. **Consumers**:
   - `process_payment`: Consumes from `payment_queue` and processes payment information.
   - `notify`: Consumes from `notification_queue` to simulate user notifications.

---

## Assumptions
- **Payment Validity**: The system assumes all payment information provided is correct and valid.

---

## Project Setup and Running

### Prerequisites
- **Docker** and **Docker Compose** must be installed on your machine.

---

### Run the Project
1. Clone the repository.
2. Run the following command in the project directory:
   ```bash
   docker-compose up
   ```
3. The FastAPI app will be available at `http://127.0.0.1:8000`.
4. RabbitMQ Management UI will be available at `http://127.0.0.1:15672`. Use `guest/guest` for username and password.

---

### Stop the Project
To stop and remove containers, networks, and volumes created by Docker Compose:
```bash
docker-compose down
```

---

## Endpoint

### **POST `/make-payment`**

- **Description**: Accepts payment information and publishes it to the `payment_queue`.
- **Content-Type**: `application/x-www-form-urlencoded`
- **Request Body**:
  - `user` (string): User's name.
  - `paymentType` (string): Payment type.
  - `cardNo` (string): Card number.

#### Example Curl Command:
```bash
curl --location 'http://127.0.0.1:8000/make-payment' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'user=user-back-end Buckinghamshire Tuna' \
--data-urlencode 'paymentType=72326079' \
--data-urlencode 'cardNo=824'
```

---

### Response Example
- **Success**:
  ```json
  {
    "status": "Payment request sent"
  }
  ```
- **Error**: If any field is missing or invalid:
  ```json
  {
    "detail": "EMPTY FIELD"
  }
  ```

---

## Key Notes
- **Port Mapping**:
  - FastAPI service: `8000`
  - RabbitMQ Management UI: `15672`
- **Dependencies**:
  - Python version: `3.11`
  - Refer to `requirements.txt` for all Python dependencies.
- **Docker**: The project includes a `Dockerfile` and `docker-compose.yaml` to streamline deployment.

---

## RabbitMQ Configuration
- RabbitMQ is preconfigured with default credentials (`guest/guest`) and two queues:
  - `payment_queue`
  - `notification_queue`

Ensure RabbitMQ is running and accessible for the FastAPI service to function correctly.
