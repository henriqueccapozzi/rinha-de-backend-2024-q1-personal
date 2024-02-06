from django.http import JsonResponse
from django.shortcuts import get_object_or_404

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

        # Redirect to a success page or do any other necessary processing

    return JsonResponse(data=transaction.to_json(), status=200)
    return JsonResponse({"message": "Transaction created successfully"}, status=200)
