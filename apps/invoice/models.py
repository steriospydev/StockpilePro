from django.core.validators import MinValueValidator
from django.db import models

from ..product.models import Product
from ..supplier.models import Supplier


class TimeStamp(models.Model):
    created_at = models.DateTimeField('Δημιουργηθηκε', auto_now_add=True)
    updated_at = models.DateTimeField('Ανανεωθηκε', auto_now=True)

    class Meta:
        abstract = True

class Invoice(TimeStamp):
    invoice_no = models.BigIntegerField('Invoice No', unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date_of_issuance = models.DateTimeField('Ημερομηνία')
    subtotal = models.DecimalField('Μερικό Σύνολο', max_digits=12, decimal_places=2, blank=True, default=0)
    total_taxes = models.DecimalField('ΦΠΑ', max_digits=12, decimal_places=2, blank=True, default=0)
    total = models.DecimalField('Συνολο', max_digits=12, decimal_places=2, blank=True, default=0)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('invoice_no', 'supplier')

    def __str__(self):
        return f'{self.vendor} - {self.invoice_no}'

    def save(self, *args, **kwargs):
        self.subtotal = Decimal(0)
        self.total_taxes = Decimal(0)
        for item in self.invoice_items.all():
            item.save()
            self.subtotal += item.line_total
            self.total_taxes += item.total_tax
        self.total = self.subtotal + self.total_taxes
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_items', on_delete=models.CASCADE)
    quantity = models.BigIntegerField('Ποσότητα', default=0, validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField('ΦΠΑ %', max_digits=8, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_tax = models.DecimalField('Φορος', max_digits=8, decimal_places=2, default=0)
    unit_price = models.DecimalField('Τιμή Μονάδας', max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    line_total = models.DecimalField('Price', max_digits=12, decimal_places=2, blank=True)

    class Meta:
        unique_together = ('invoice', 'product')

    def __str__(self):
        return f'{self.product}'

    def get_tax_rate(self):
        # Retrieve tax_rate from product.tax and store to tax_rate
        return self.product.tax

    def get_tax_total(self):
        # Calculate total_tax = quantity * ((tax_rate/100) * unit_price)
        tax_rate_decimal = Decimal(self.tax_rate) / Decimal(100)
        return self.quantity * (tax_rate_decimal * self.unit_price)

    def get_line_total(self):
        # Calculate line_total = (quantity * unit_price) + tax_total
        self.tax_rate = self.get_tax_rate()
        self.total_tax = self.get_tax_total()
        self.line_total = (self.quantity * self.unit_price) + self.total_tax
        self.save()
        return self.line_total

    def save(self, *args, **kwargs):
        self.line_total = self.get_line_total()
        super().save(*args, **kwargs)
        self.invoice.save()
