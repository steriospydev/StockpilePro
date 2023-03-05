from django.contrib import admin
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'invoice_no',
                    'date_of_issuance',
                    'subtotal', 'total_taxes']
    inlines = [InvoiceItemInline]

    def total(self, obj):
        return sum([item.amount for item in obj.items.all()])

    total.short_description = 'Total Amount'


admin.site.register(Invoice, InvoiceAdmin)

# προιον | Ποσοτητα |Τιμη   |   ΦΠΑ |  Φορος | ολικο
# Αυρα   |  10      | 1.00  |   13% |   1,30 |  10
