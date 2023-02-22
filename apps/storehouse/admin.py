from django.contrib import admin
from .models import Storage, Section, Spot, Bin


admin.site.register(Section)
admin.site.register(Spot)

class StorageAdmin(admin.ModelAdmin):
    model = Storage
    list_display = ('storage_name', 'capacity', 'summary',
                    'location',)

class BinAdmin(admin.ModelAdmin):
    model = Bin
    list_display = ('__str__', 'storage', 'in_use', 'updated_at')


admin.site.register(Storage, StorageAdmin)
admin.site.register(Bin, BinAdmin)
