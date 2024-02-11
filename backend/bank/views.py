from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .utils import get_client_balance_and_metadata

# Create your views here.


# view to create transactions for a given client
from .models import Client, Transaction


def create_transaction(request, client_id):
    # Retrieve the client based on the client_id
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        # Extract the transaction details from the request data
        amount = request.POST.get("amount")
        type = request.POST.get("type")
        description = request.POST.get("description")

        # Create a new transaction object
        transaction = Transaction.objects.create(
            amount=amount, type=type, description=description, client=client
        )
        # transaction.save()
        client_metadata = get_client_balance_and_metadata(client_id)

        # Redirect to a success page or do any other necessary processing

    result_obj = {
        "limite": client_metadata["limit"],
        "saldo": client_metadata["current_balance"],
    }
    return JsonResponse(data=result_obj, status=200)
    return JsonResponse({"message": "Transaction created successfully"}, status=200)


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
