import random
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from apps.utils import signals
from ..invoice.models import InvoiceItem

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField('Δημιουργηθηκε', auto_now_add=True)
    updated_at = models.DateTimeField('Ανανεωθηκε', auto_now=True)

    class Meta:
        abstract = True

class BinType(models.Model):
    SHELF = 'S'
    FLOOR = 'F'
    BIN_TYPE_CHOICES = [
        (SHELF, 'Shelf'),
        (FLOOR, 'Floor'),
    ]

    bin_type = models.CharField(
        max_length=1,
        choices=BIN_TYPE_CHOICES,
        default=FLOOR,
    )

    class Meta:
        abstract = True

class Storage(TimeStamp):
    storage_name = models.CharField("Ονομασία",
                                    unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The storage name must be a'
                                                ' single uppercase letter from'
                                                ' A to Z',
                                        code='invalid_storage_name')])
    capacity = models.CharField("Χωρητικότητα", max_length=120, blank=True, null=True)
    location = models.CharField("Τοποθεσια", max_length=120, blank=True, null=True)
    summary = models.TextField("Περιγραφή", blank=True, null=True)

    class Meta:
        verbose_name = 'Αποθηκη'
        verbose_name_plural = 'Αποθηκες'

    def __str__(self):
        return f'{self.storage_name}'

class Section(TimeStamp):
    section_name = models.CharField('Μπλόκ', unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The section name'
                                                ' must be a single uppercase'
                                                ' letter from A to Z',
                                        code='invalid_storage_name')])

    class Meta:
        verbose_name = 'Διαδρομος'
        verbose_name_plural = 'Διαδρομοι'

    def __str__(self):
        return f'{self.section_name}'

class Spot(TimeStamp):
    spot_name = models.CharField('Θεση', unique=True,
                                 max_length=3,
                                 default='000',
                                 validators=[RegexValidator(
                                     regex=r'^[0-9]{3}$',
                                     message='Η τιμή πρέπει να είναι από '
                                             '001 έως 999', )]
                                 )

    class Meta:
        verbose_name = 'Θεση'
        verbose_name_plural = 'Θεσεις'

    def __str__(self):
        return f'{self.spot_name}'

class UseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(in_use=True)

class Bin(TimeStamp, BinType):
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE,
                                related_name='storage_bins')
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                related_name='section_bins')
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE, related_name='spot_bins')
    in_use = models.BooleanField('Σε χρηση', default=False)

    objects = models.Manager()
    occupied = UseManager()

    class Meta:
        verbose_name = 'Θεση αποθηκευσης'
        verbose_name_plural = 'Θεσεις αποθηκευσης'
        constraints = [
            models.UniqueConstraint(fields=['storage', 'section', 'spot', 'bin_type'],
                                    name='unique_bin')]
        ordering = ['storage', 'section', 'bin_type', 'spot']

    def __str__(self):
        return f'{self.storage}/{self.section}-{self.spot}{self.bin_type}'


class StockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('item')

class Stock(TimeStamp):
    item = models.OneToOneField(InvoiceItem, on_delete=models.CASCADE,
                                related_name='invoice_stock')
    expiration_date = models.DateField('Ημ.Ληξης', null=True)

    start_quantity = models.DecimalField('Αρχικη Ποσοτητα', max_digits=12,
                                         decimal_places=2, default=0)
    stock_placed = models.DecimalField('Τοποθετημένο στοκ', max_digits=12,
                                       decimal_places=2, default=0)
    retrieved = models.DecimalField('Εξαγωγη', max_digits=12,
                                    decimal_places=2, default=0)

    is_placed = models.BooleanField('Τοποθετηση', default=False)
    deplete = models.BooleanField('Εξαντλημενο', default=False)

    sku = models.CharField('SKU', max_length=9, unique=True,
                           blank=True, null=True, editable=False)

    objects = StockManager()

    class Meta:
        verbose_name = 'Στοκ'
        verbose_name_plural = 'Στοκ'
        ordering = ['expiration_date']

    def __str__(self):
        return f'{self.item}/{self.sku}'

    def get_absolute_url(self):
        return reverse('storehouse:stock-detail', args=[str(self.id)])

    def get_unique_number(self, prefix):
        while True:
            # generate a random 3-digit number
            number = str(random.randint(0, 999)).zfill(3)
            sku = f"{prefix}-{number}"
            # check if the sku is already taken
            if not Stock.objects.filter(sku=sku).exists():
                return number

    def generate_sku_num(self):
        part_1 = f"{self.item.invoice.supplier.sku_num}{self.item.product.sku_num}"
        part_2 = self.get_unique_number(part_1)
        return f"{part_1}-{part_2}"

    def get_start_quantity(self):
        return self.item.quantity

    def change_deplete_status(self):
        if self.retrieved >= self.start_quantity:
            self.retrieved = self.start_quantity
            return True
        return False

    def stock_is_placed(self):
        if self.stock_placed == self.start_quantity:
            return True
        return False

    def save(self, *args, **kwargs):
        self.start_quantity = self.get_start_quantity()
        self.deplete = self.change_deplete_status()
        self.is_placed = self.stock_is_placed()
        super().save(*args, **kwargs)

class PlaceStock(TimeStamp):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE,
                              related_name='place_stock')
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE,
                            related_name='stock_bin')
    deplete = models.BooleanField('Εξαντλημενο', default=False)
    quantity = models.DecimalField("Ποσότητα", max_digits=8,
                                   decimal_places=2, default=0)
    exit_stock = models.DecimalField('Εξαγωγη', max_digits=12,
                                     decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Τοποθετηση'
        verbose_name_plural = 'Τοποθετησεις'
        ordering = ['stock__expiration_date']

    def update_stock_stock_placed(self):
        max_stock_left = self.stock.start_quantity - self.stock.stock_placed
        if self.quantity >= max_stock_left:
            self.quantity = max_stock_left
            self.stock.stock_placed = self.stock.start_quantity
        if self.quantity < max_stock_left:
            self.stock.stock_placed += self.quantity

        self.stock.save()

    def update_bin_use(self):
        if self.exit_stock == self.quantity:
            self.bin.in_use = False
            self.deplete = True
        else:
            self.bin.in_use = True
        self.bin.save()

    def validate_exit_stock(self):
        if self.exit_stock >= self.quantity:
            self.exit_stock = self.quantity
        return

    def update_stock_retrieved(self):
        objs = PlaceStock.objects.filter(stock=self.stock)
        sum_retrieved = 0
        for obj in objs:
            sum_retrieved += obj.exit_stock
        self.stock.retrieved = sum_retrieved
        self.stock.save()

    def save(self, *args, **kwargs):
        if not self.stock.is_placed:
            self.update_stock_stock_placed()
        self.validate_exit_stock()
        self.update_bin_use()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Calculate the new stock_placed value
        self.stock.stock_placed -= self.quantity
        if self.stock.stock_placed < 0:
            self.stock.stock_placed = 0
        self.stock.is_placed = False

        # Save the changes to the Stock object
        self.stock.save()

        # Call the superclass delete method to delete the PlaceStock object
        super().delete(*args, **kwargs)


# signals


@receiver(pre_save, sender=Stock)
def generate_stock_sku(sender, instance, *args, **kwargs):
    if not instance.sku:
        instance.sku = instance.generate_sku_num()

@receiver(post_save, sender=InvoiceItem)
def create_or_update_stock(sender, instance, created, **kwargs):
    if created:
        stock = Stock.objects.create(item=instance)
        stock.save()
    else:
        try:
            stock = Stock.objects.get(item=instance)
        except Stock.DoesNotExist:
            return
        stock.quantity = instance.quantity
        stock.save()

@receiver(pre_save, sender=PlaceStock)
def update_stock_retrieved_on_save(sender, instance, **kwargs):
    # Calculate the new stock_placed value
    instance.update_stock_retrieved()

    # Save the changes to the Stock object
    instance.stock.save()


@receiver(pre_delete, sender=PlaceStock)
def update_stock_on_placestock_delete(sender, instance, **kwargs):
    # Calculate the new stock_placed value
    instance.stock.stock_placed -= instance.quantity
    instance.bin.in_use = False
    instance.bin.save()
    if instance.stock.stock_placed < 0:
        instance.stock.stock_placed = 0
    instance.stock.is_placed = False

    # Save the changes to the Stock object
    instance.stock.save()

@receiver(post_save, sender=PlaceStock)
def update_exit_stock(sender, instance, **kwargs):
    if instance.exit_stock >= instance.quantity:
        instance.exit_stock = instance.quantity
        instance.bin.in_use = False
        instance.deplete = True
    instance.stock.retrieved += instance.exit_stock
    instance.stock.save()
    instance.bin.save()

@receiver(pre_delete, sender=InvoiceItem)
def delete_stock_instance(sender, instance, **kwargs):
    stock = Stock.objects.get(item=instance)

    # Delete all PlaceStock objects that are connected to the Stock object
    place_stocks = PlaceStock.objects.filter(stock=stock)
    place_stocks.delete()

    # Delete the Stock object
    stock.delete()
