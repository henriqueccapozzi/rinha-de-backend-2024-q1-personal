from datetime import datetime
from django.db.models import Sum, Case, When, F

from .models import Client, Transaction


def get_client_balance_and_metadata(client_id):
    client = Client.objects.get(id=client_id)
    total_deposit = Transaction.objects.filter(client_id=client_id, type="c").aggregate(
        total_deposit=Sum("amount")
    )
    total_withdrawal = Transaction.objects.filter(client_id=client_id, type="d").aggregate(
        total_withdrawal=Sum("amount")
    )

    total_deposit_amount = total_deposit["total_deposit"] or 0
    total_withdrawal_amount = total_withdrawal["total_withdrawal"] or 0
    initial_balance = client.initial_balance or 0

    current_balance = total_deposit_amount - total_withdrawal_amount + initial_balance

    client_metadata = {
        "current_balance": current_balance,
        "limit": client.limit,
        "balance_date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }

    return client_metadata
