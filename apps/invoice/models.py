from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from ..product.models import Product
from ..supplier.models import Supplier


class TimeStamp(models.Model):
    created_at = models.DateTimeField('Δημιουργηθηκε', auto_now_add=True)
    updated_at = models.DateTimeField('Ανανεωθηκε', auto_now=True)

    class Meta:
        abstract = True

class Invoice(TimeStamp):
    invoice_no = models.BigIntegerField('Invoice No')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date_of_issuance = models.DateTimeField('Ημερομηνία')
    subtotal = models.DecimalField('Μερικό Σύνολο', max_digits=12, decimal_places=2, blank=True, default=0)
    total_taxes = models.DecimalField('ΦΠΑ', max_digits=12, decimal_places=2, blank=True, default=0)
    total = models.DecimalField('Συνολο', max_digits=12, decimal_places=2, blank=True, default=0)

    class Meta:
        verbose_name = "Τιμολογιο"
        verbose_name_plural = "Τιμολογια"
        ordering = ('-created_at',)
        unique_together = ('invoice_no', 'supplier')

    def __str__(self):
        return f'{self.supplier} - {self.invoice_no}'

    def calculate_total_taxes(self):
        self.total_taxes = sum([item.get_tax_total() for item in self.invoice_items.all()])
        return self.total_taxes

    def calculate_subtotal(self):
        self.subtotal = sum([item.get_line_total() - item.get_tax_total() for item in self.invoice_items.all()])
        return self.subtotal

    def calculate_total(self):
        self.total = sum([item.get_line_total() for item in self.invoice_items.all()])
        return self.total

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.subtotal = self.calculate_subtotal()
        self.total_taxes = self.calculate_total_taxes()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)



class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_items', on_delete=models.CASCADE)
    quantity = models.FloatField('Ποσότητα', default=00.00, validators=[MinValueValidator(0)])
    tax_rate = models.FloatField('ΦΠΑ %', default=00.00, validators=[MinValueValidator(0)])
    total_tax = models.FloatField('Φορος', default=00.00)
    unit_price = models.FloatField('Τιμή Μονάδας', default=00.00, validators=[MinValueValidator(0)])
    line_total = models.FloatField('Τιμη', default=00.00, blank=True)

    class Meta:
        unique_together = ('invoice', 'product')

    def __str__(self):
        return f'{self.product}'

    def get_tax_rate(self):
        return self.product.tax_rate.value

    def get_tax_total(self):
        self.total_tax = self.quantity * ((self.tax_rate/100) * self.unit_price)
        return self.total_tax

    def get_line_total(self):
        self.line_total = (self.quantity * self.unit_price) + self.get_tax_total()
        return self.line_total

    def save(self, *args, **kwargs):
        self.tax_rate = self.get_tax_rate()
        self.total_tax = self.get_tax_total()
        self.line_total = self.get_line_total()
        super().save(*args, **kwargs)
