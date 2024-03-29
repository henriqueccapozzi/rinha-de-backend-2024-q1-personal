from datetime import datetime
import json

from django.db.models import Sum, Case, When, F
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .utils import check_transaction_data, get_client_balance_and_metadata

# Create your views here.


# view to create transactions for a given client
from .models import Client, Transaction


def create_transaction(request, client_id):
    if request.method == "POST":
        # Extract the transaction details from the request data
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        amount = body.get("valor")
        type = body.get("tipo")
        description = body.get("descricao", "")
        transaction_data = {"amount": amount, "type": type, "description": description}
        success = check_transaction_data(transaction_data)
        if not success:
            return JsonResponse(data={}, status=422)

        # Only go to the DB if the received data passes basic validation
        with transaction.atomic():
            try:
                client = Client.objects.select_for_update().get(id=client_id)
            except Client.DoesNotExist:
                return JsonResponse(data={}, status=404)
            current_balance = client.current_balance
            if type == "d":
                if amount > current_balance + client.limit:
                    return JsonResponse(data={}, status=422)

            new_balance = current_balance
            if type == "d":
                new_balance = current_balance - amount
            elif type == "c":
                new_balance = current_balance + amount

            client.current_balance = new_balance
            client.save()
            bank_transaction = Transaction.objects.create(
                amount=amount, type=type, description=description, client=client
            )
            # bank_transaction.save()
            result_obj = {
                "limite": client.limit,
                "saldo": new_balance,
            }
            return JsonResponse(data=result_obj, status=200)


def get_bank_statement(request, client_id, limit_transactions=10):
    with transaction.atomic():
        client = get_object_or_404(Client, id=client_id)
        balance_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        current_balance = client.current_balance

        client_metadata = {
            "current_balance": current_balance,
            "limit": client.limit,
            "balance_date": balance_date,
        }
        last_transactions = (
            Transaction.objects.filter(client=client_id)
            .order_by("-created_at")
            .only("amount", "type", "description", "created_at")[:limit_transactions]
        )
        data_to_return = {
            "saldo": {
                "total": client_metadata["current_balance"],
                "data_extrato": client_metadata["balance_date"],
                "limite": client_metadata["limit"],
            },
            "ultimas_transacoes": [t.to_summarized_json() for t in last_transactions],
        }

        return JsonResponse(
            data=data_to_return,
        )
        pass
