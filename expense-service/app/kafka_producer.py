import json
import os
from confluent_kafka import Producer
from datetime import datetime

_producer = None

def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
        })
    return _producer

def publish_expense_created(
        group_id: str,
        expense_id: str,
        paid_by_name: str,
        amount: float,
        description: str,
        created_at: datetime,
        recipient_emails: list[str]
):
    message = {
        "group_id": group_id,
        "expense_id": expense_id,
        "paid_by_name": paid_by_name,
        "amount": amount,
        "description": description,
        "created_at": created_at.isoformat(),
        "recipient_emails": recipient_emails
    }
    get_producer().produce(
        topic="expense-created",
        key=str(group_id),
        value=json.dumps(message).encode("utf-8")
    )
    get_producer().flush()