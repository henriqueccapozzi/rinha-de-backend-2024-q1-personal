from django.db import models
from datetime import datetime

# Create your models here.
class Transaction(models.Model):
    class TransactionTypeChoices(models.TextChoices):
        CREDITO = "c", "Credito"
        DEBITO = "d", "Debito"

    amount = models.IntegerField()
    type = models.CharField(max_length=1, choices=TransactionTypeChoices.choices)
    description = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=datetime.utcnow)
    client = models.ForeignKey("Client", on_delete=models.CASCADE)

    def to_json(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at,
            "client": self.client.to_json(),
        }


class Client(models.Model):
    limit = models.IntegerField()
    initial_balance = models.IntegerField()

    def to_json(self):
        return {
            "id": self.id,
            "limit": self.limit,
            "initial_balance": self.initial_balance,
        }
