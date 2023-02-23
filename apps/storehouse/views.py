from django.shortcuts import render
from django.db.models import Count, Q
from .models import Storage, Section, Spot, Bin
# Create your views here.

def storehouse_home(request):

    storages = Storage.objects.annotate(total_sections=Count('bin__section', distinct=True))
    bins_agg = Bin.objects.aggregate(
        total_bins=Count('id'),
        bins_in_use=Count('id', filter=Q(in_use=True))
    )
    bins_occupied = bins_agg['total_bins'] - bins_agg['bins_in_use']

    storage_count = storages.annotate(
        total_bins=Count('bin'),
        storage_bins_in_use=Count('bin', filter=Q(bin__in_use=True))
    ).values(
        'id',
        'storage_name',
        'total_sections',
        'total_bins',
        'storage_bins_in_use'
    )

    for storage in storage_count:
        storage['free_bins'] = storage['total_bins'] - storage['storage_bins_in_use']

    context = {
        'storages': storages.count(),
        'total_bins': bins_agg['total_bins'],
        'bins_in_use': bins_agg['bins_in_use'],
        'bins_occupied': bins_occupied,
        'storage_count': storage_count
    }
    return render(request, 'storehouse/storehouse_main.html', context)
