from django.shortcuts import render
from django.db.models import Count, Q
from .models import Storage, Section, Spot, Bin
# Create your views here.

def storehouse_home(request):
    storages = Storage.objects.aggregate(total_storages=Count('id'))
    bins = Bin.objects.aggregate(
        total_bins=Count('id'),
        bins_in_use=Count('id', filter=Q(in_use=True))
    )
    bins_occupied = bins['total_bins'] - bins['bins_in_use']

    context = {
        'storages': storages['total_storages'],
        'total_bins': bins['total_bins'],
        'bins_in_use': bins['bins_in_use'],
        'bins_occupied': bins_occupied
    }

    # list of storage - total of sections in
    return render(request, 'storehouse/storehouse_main.html', context)
