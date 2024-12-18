# Assignment 2 Queue - Payment Processing Service

### Overview

This project is a **payment processing service** built with **FastAPI** and **RabbitMQ**. The service allows users to submit payment information, processes these payments asynchronously, and sends notifications once payments are successfully processed.

---

### Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Start the services** using Docker Compose:
   ```bash
   docker-compose up
   ```

3. **RabbitMQ Management UI**:
   - Accessible at `http://127.0.0.1:15672` with credentials:
     - Username: `guest`
     - Password: `guest`

4. **FastAPI Application**:
   - Accessible at `http://127.0.0.1:8000`.

5. **Stop the services**:
   ```bash
   docker-compose down
   ```

---

### Production

- The application is containerized and can be deployed using Docker or similar orchestration platforms.

---

### Routes

| **Route**               | **Description**                                                                 |
|--------------------------|---------------------------------------------------------------------------------|
| `GET /`                 | Root endpoint. Returns a simple "Hello World" message.                          |
| `POST /make-payment`    | Accepts payment information and sends it to the `payment_queue` for processing. |

#### Example Curl Command
```bash
curl --location 'http://127.0.0.1:8000/make-payment' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'user=user-back-end Buckinghamshire Tuna' \
--data-urlencode 'paymentType=72326079' \
--data-urlencode 'cardNo=824'
```

---

### Assumptions

- **Payment Validity**: The system assumes that all provided payment information is correct and valid.

---

### Features

- **Asynchronous Processing**: Payment requests are processed asynchronously using RabbitMQ.
- **Queue-Based Architecture**:
  - `payment_queue`: Handles incoming payment requests.
  - `notification_queue`: Sends notifications after successful payment processing.

---

### RabbitMQ Configuration

- RabbitMQ is configured with:
  - Two queues: `payment_queue` and `notification_queue`.
  - Default credentials: `guest/guest`.

---

### Documentation

- **YouTube Presentation & Explanation**: [YouTube Link](https://youtu.be/8dTybm3kJK8)
