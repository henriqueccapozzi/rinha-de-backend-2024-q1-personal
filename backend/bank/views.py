import json

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
        client = get_object_or_404(Client, id=client_id)
        with transaction.atomic():
            client_metadata = get_client_balance_and_metadata(client_id)
            if type == "d":
                current_balance = client_metadata["current_balance"]

                if amount > current_balance + client.limit:
                    return JsonResponse(data={}, status=422)

            bank_transaction = Transaction(
                amount=amount, type=type, description=description, client=client
            )
            bank_transaction.save()
            client_metadata = get_client_balance_and_metadata(client_id)
            client_metadata["current_balance"]
            result_obj = {
                "limite": client_metadata["limit"],
                "saldo": client_metadata["current_balance"],
            }
            return JsonResponse(data=result_obj, status=200)

        client_metadata = get_client_balance_and_metadata(client_id)


def get_bank_statement(request, client_id, limit_transactions=10):
    last_transactions = Transaction.objects.filter(client=client_id).order_by("-created_at")[
        :limit_transactions
    ]
    client_metadata = get_client_balance_and_metadata(client_id)
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
