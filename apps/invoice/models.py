from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal

from django.db.models import DecimalField
from django.urls import reverse


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
        self.total_taxes = sum([item.get_tax_total for item in self.invoice_items.all()])
        return self.total_taxes

    def calculate_subtotal(self):
        self.subtotal = sum([item.get_line_subtotal() for item in self.invoice_items.all()])
        return self.subtotal

    def calculate_total(self):
        self.total = self.subtotal + self.total_taxes
        return self.total

    def get_absolute_url(self):
        return reverse('invoice:invoice-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.subtotal = self.calculate_subtotal()
        self.total_taxes = self.calculate_total_taxes()
        self.total = self.calculate_total()
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_items',
                                on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_items',
                                on_delete=models.CASCADE)
    quantity = models.DecimalField('Ποσότητα', default=00.00,
                                   max_digits=5, decimal_places=1,
                                   validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField('ΦΠΑ %', default=00.00,
                                   blank=True,
                                   max_digits=4, decimal_places=1,
                                   validators=[MinValueValidator(0)])
    total_tax = models.DecimalField('Φορος', max_digits=5, decimal_places=2,
                                    blank=True,
                                    default=00.00)
    unit_price = models.DecimalField('Τιμή Μονάδας', blank=True,
                                     max_digits=8, decimal_places=2,
                                     default=00.00, validators=[MinValueValidator(0)])
    line_subtotal = models.DecimalField('Μερικό', default=00.00,
                                        max_digits=8, decimal_places=2,
                                        blank=True)
    line_total = models.DecimalField('Τιμη', default=00.00,
                                     max_digits=8, decimal_places=2,
                                     blank=True)

    def get_absolute_url(self):
        return reverse('invoice:invoice-item-update', args=[self.invoice.id, self.id])

    class Meta:
        unique_together = ('invoice', 'product')

    def __str__(self):
        return f'{self.product}'

    def get_tax_rate(self):
        return self.product.tax_rate.value

    @property
    def get_tax_total(self):
        # noinspection PyTypeChecker
        self.total_tax = (self.quantity * (self.tax_rate / Decimal(100)) * self.unit_price).quantize(Decimal(
            '0.00'))
        return self.total_tax

    def get_line_subtotal(self):
        self.line_subtotal = (self.quantity * self.unit_price)
        return self.line_subtotal

    def save(self, *args, **kwargs):
        self.tax_rate = self.get_tax_rate()
        self.total_tax = self.get_tax_total
        self.line_subtotal = self.get_line_subtotal()
        self.line_total = self.line_subtotal + self.total_tax
        super().save(*args, **kwargs)
