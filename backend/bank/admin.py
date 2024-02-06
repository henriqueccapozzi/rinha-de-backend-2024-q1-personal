from django.contrib import admin

# Register your models here.
from .models import Client, Transaction

admin.site.register(Client)
admin.site.register(Transaction)
