from django.shortcuts import render
from django.db.models import Count, Q, Case, When, BooleanField

from .models import Storage, Section, Spot, Bin

def storehouse_home(request):
    storages = Storage.objects.prefetch_related('bins').annotate(
        total_sections=Count('bins__section', distinct=True))

    bins_agg = Bin.objects.aggregate(
        total_bins=Count('id'),
        bins_in_use=Count('id', filter=Q(in_use=True))
    )
    bins_occupied = bins_agg['total_bins'] - bins_agg['bins_in_use']

    storage_count = storages.annotate(
        total_bins=Count('bins'),
        storage_bins_in_use=Count('bins', filter=Q(bins__in_use=True))
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


def storage_bins_page(request, pk):
    #
    storage = Storage.objects.prefetch_related(
        'bins', 'bins__section').get(id=pk)

    bins = storage.bins.select_related('section', 'spot').annotate(
        is_free=Case(
            When(in_use=False, then=True),
            default=False,
            output_field=BooleanField()))

    # Count available bins
    all_bins = storage.bins.count()
    free_bins = storage.bins.filter(in_use=False).count()
    in_use_bins = all_bins - free_bins

    # Available bin depending on type
    shelves_available = storage.bins.filter(bin_type='S', in_use=False).count()
    floor_available = storage.bins.filter(bin_type='F', in_use=False).count()

    context = {
        'bins': bins,
        'storage': storage,
        'all_bins': all_bins,
        'free_bins': free_bins,
        'in_use_bins': in_use_bins,
        'free_shelves': shelves_available,
        'free_floor': floor_available
    }
    return render(request, 'storehouse/storehouse_detail.html', context)
