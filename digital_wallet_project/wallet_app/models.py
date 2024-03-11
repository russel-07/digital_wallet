from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Wallet(models.Model):

    PAYMENT_SYSTEMS = (
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard')
    )

    WALLET_CURRENCIES = (
        ('rub', 'RUB'),
        ('usd', 'USD'),
        ('eur', 'EUR')
    )

    name = models.CharField(max_length=8, unique=True, verbose_name='Имя')
    payment_system = models.CharField(max_length=20, choices=PAYMENT_SYSTEMS,
                                      verbose_name='Платежная система')
    currency = models.CharField(max_length=20, choices=WALLET_CURRENCIES,
                                verbose_name='Валюта')
    balance = models.DecimalField(max_digits=20, decimal_places=2,
                                  verbose_name='Баланс', default=0.00)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='wallets',
                              verbose_name='Собственник')
    created_on = models.DateTimeField('Дата создания', auto_now_add=True)
    modified_on = models.DateTimeField('Дата изменения', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Кошелек'
        verbose_name_plural = 'Кошельки'
        ordering = ['-created_on']


class Transaction(models.Model):

    TRANSACTION_STATUSES = (
        ('paid', 'PAID'),
        ('failed', 'FAILED')
    )

    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                               related_name='outgoing_transactions',
                               verbose_name='Кошелек отправителя')
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                                 related_name='incoming_transactions',
                                 verbose_name='Кошелек получателя')
    transfer_amount = models.DecimalField(max_digits=20, decimal_places=2,
                                          verbose_name='Сумма перевода')
    commission = models.DecimalField(max_digits=20, decimal_places=2,
                                     verbose_name='Комиссия')
    status = models.CharField(max_length=10, choices=TRANSACTION_STATUSES,
                              verbose_name='Статус операции')
    timestamp = models.DateTimeField('Время операции', auto_now_add=True)

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
        ordering = ['-timestamp']
