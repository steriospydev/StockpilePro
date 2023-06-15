import random
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from apps.utils import signals
from ..invoice.models import InvoiceItem


# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

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
    storage_name = models.CharField("Storage Name",
                                    unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The storage name must be a'
                                                ' single uppercase letter from'
                                                ' A to Z',
                                        code='invalid_storage_name')])
    capacity = models.CharField("Capacity", max_length=120, blank=True, null=True)
    location = models.CharField("Location", max_length=120, blank=True, null=True)
    summary = models.TextField("Description", blank=True, null=True)

    class Meta:
        verbose_name = 'Storage'
        verbose_name_plural = 'Storages'

    def __str__(self):
        return f'{self.storage_name}'


class Section(TimeStamp):
    section_name = models.CharField('Lane', unique=True,
                                    max_length=1,
                                    validators=[RegexValidator(
                                        regex=r'^[A-Z]$',
                                        message='The section name'
                                                ' must be a single uppercase'
                                                ' letter from A to Z',
                                        code='invalid_storage_name')])

    class Meta:
        verbose_name = 'Lane'
        verbose_name_plural = 'Lanes'

    def __str__(self):
        return f'{self.section_name}'


class Spot(TimeStamp):
    spot_name = models.CharField('Spot', unique=True,
                                 max_length=3,
                                 default='000',
                                 validators=[RegexValidator(
                                     regex=r'^[0-9]{3}$',
                                     message='Value must be'
                                             '001 - 999', )]
                                 )

    class Meta:
        verbose_name = 'Spot'
        verbose_name_plural = 'Spots'

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
    in_use = models.BooleanField('In Use', default=False)

    objects = models.Manager()
    occupied = UseManager()

    class Meta:
        verbose_name = 'Bin'
        verbose_name_plural = 'Bins'
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
    expiration_date = models.DateField('Exp.Date', null=True)

    start_quantity = models.DecimalField('Start Quantity', max_digits=12,
                                         decimal_places=2, default=0)
    stock_placed = models.DecimalField('Placed', max_digits=12,
                                       decimal_places=2, default=0)
    retrieved = models.DecimalField('Extracted', max_digits=12,
                                    decimal_places=2, default=0)

    is_placed = models.BooleanField('Placed', default=False)
    deplete = models.BooleanField('Deplete', default=False)

    sku = models.CharField('SKU', max_length=9, unique=True,
                           blank=True, null=True, editable=False)

    objects = StockManager()

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stock'
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
    deplete = models.BooleanField('Deplete', default=False)
    quantity = models.DecimalField("Quantity", max_digits=8,
                                   decimal_places=2, default=0)
    exit_stock = models.DecimalField('Extracted', max_digits=12,
                                     decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Placement'
        verbose_name_plural = 'Placements'
        ordering = ['stock__expiration_date']

    def get_absolute_url(self):
        return reverse('storehouse:stock-exit', kwargs={'pk': self.id})

    def validate_quantity(self):
        total_quantity = PlaceStock.objects.filter(stock=self.stock).exclude(pk=self.pk).aggregate(Sum('quantity'))['quantity__sum'] or 0
        available_quantity = self.stock.start_quantity - total_quantity
        if self.quantity > available_quantity:
            self.quantity = available_quantity
        return self.quantity

    def validate_exit_stock(self):
        if self.exit_stock > self.quantity:
            return self.quantity
        return self.exit_stock

    def save(self, *args, **kwargs):
        self.quantity = self.validate_quantity()
        self.exit_stock = self.validate_exit_stock()
        super().save(*args, **kwargs)


# signals
@receiver([post_save, post_delete], sender=PlaceStock)
def update_stock_stock_placed(sender, instance, *args, **kwargs):
    objs = PlaceStock.objects.filter(stock=instance.stock)
    pstock = 0
    ex_stock = 0
    for item in objs:
        pstock += item.quantity
        ex_stock += item.exit_stock
    instance.stock.stock_placed = pstock
    instance.stock.retrieved = ex_stock
    instance.stock.save()

@receiver([pre_save, pre_delete], sender=PlaceStock)
def stock_deplete(sender, instance, *args, **kwargs):
    if instance.quantity == instance.exit_stock and instance.exit_stock != 0:
        instance.bin.in_use = False
        instance.deplete = True
    else:
        instance.bin.in_use = True
        instance.deplete = False
    instance.bin.save()

@receiver(pre_delete, sender=PlaceStock)
def bin_update_on_delete(sender, instance, *args, **kwargs):
    instance.bin.in_use = False
    instance.bin.save()

@receiver(pre_save, sender=PlaceStock)
def bin_update_on_change(sender, instance, *args, **kwargs):
    # If the instance is being updated
    if instance.pk:
        # Get the old instance from the database
        old_instance = PlaceStock.objects.get(pk=instance.pk)
        # If the bin has changed
        if old_instance.bin != instance.bin:
            # Set the in_use field of the old bin to False
            old_bin = old_instance.bin
            old_bin.in_use = False
            old_bin.save()
            # Set the in_use field of the new bin to True
            new_bin = instance.bin
            new_bin.in_use = True
            new_bin.save()

# Signal from Stock
@receiver(pre_save, sender=Stock)
def generate_stock_sku(sender, instance, *args, **kwargs):
    if not instance.sku:
        instance.sku = instance.generate_sku_num()


# Signals from InvoiceItem
@receiver(post_save, sender=InvoiceItem)
def create_or_update_stock(sender, instance, created, **kwargs):
    try:
        stock = instance.invoice_stock
    except Stock.DoesNotExist:
        stock = None

    if created or stock is None:
        stock = Stock.objects.create(item=instance)
    else:
        stock.start_quantity = instance.quantity
        stock.save()


@receiver(pre_delete, sender=InvoiceItem)
def delete_stock_instance(sender, instance, **kwargs):
    stock = Stock.objects.get(item=instance)

    # Delete all PlaceStock objects that are connected to the Stock object
    place_stocks = PlaceStock.objects.filter(stock=stock)
    place_stocks.delete()

    # Delete the Stock object
    stock.delete()
