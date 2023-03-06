from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    fields = ['product', 'quantity', 'unit_price',
              'total_tax', 'line_total', 'tax_rate']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'invoice_no',
                    'date_of_issuance',
                    'total', 'total_taxes']
    inlines = [InvoiceItemInline]


# προιον | Ποσοτητα |Τιμη   |   ΦΠΑ |  Φορος | ολικο
# Αυρα   |  10      | 1.00  |   13% |   1,30 |  10
