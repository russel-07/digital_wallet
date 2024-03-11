from django.contrib import admin

from .models import Wallet, Transaction


class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'payment_system', 'currency', 'balance',
                    'owner', 'created_on', 'modified_on')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'transfer_amount',
                    'commission', 'status', 'timestamp')


admin.site.register(Wallet, WalletAdmin)
admin.site.register(Transaction, TransactionAdmin)
