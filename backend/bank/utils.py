from datetime import datetime
from django.db.models import Sum, Case, When, F
from django.shortcuts import get_object_or_404

from .models import Client, Transaction


def check_transaction_data(transaction_data):
    if transaction_data["amount"] <= 0:
        return False
    if type(transaction_data["amount"]) != int:
        return False
    if transaction_data["type"] not in ["c", "d"]:
        return False
    if transaction_data["description"] == None:
        return False
    if transaction_data["description"] == "":
        return False
    if len(transaction_data["description"]) > 10:
        return False
    return True


def get_client_balance_and_metadata(client_id):
    client = get_object_or_404(Client, id=client_id)
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
