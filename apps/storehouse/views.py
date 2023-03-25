from django.shortcuts import render
from django.shortcuts import reverse

from django.db.models import Count, Q, Case, When, BooleanField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Coalesce
from django.contrib.postgres.search import SearchVector

from .models import (Storage, Bin, Section, Spot,
                     Stock, PlaceStock)
from .forms import StockForm

def storehouse_home(request):
    storages = Storage.objects.prefetch_related('storage_bins').annotate(
        total_sections=Count('storage_bins__section', distinct=True))

    bins_agg = Bin.objects.aggregate(
        total_bins=Count('id'),
        bins_in_use=Count('id', filter=Q(in_use=True))
    )
    bins_occupied = bins_agg['total_bins'] - bins_agg['bins_in_use']

    storage_count = storages.annotate(
        total_bins=Count('storage_bins'),
        storage_bins_in_use=Count('storage_bins', filter=Q(storage_bins__in_use=True))
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
        'storage_bins', 'storage_bins__section').get(id=pk)

    bins = storage.storage_bins.select_related('section', 'spot').annotate(
        is_free=Case(
            When(in_use=False, then=True),
            default=False,
            output_field=BooleanField()))

    # Count available bins
    all_bins = storage.storage_bins.count()
    free_bins = storage.storage_bins.filter(in_use=False).count()
    in_use_bins = all_bins - free_bins

    # Available bin depending on type
    shelves_available = storage.storage_bins.filter(bin_type='S', in_use=False).count()
    floor_available = storage.storage_bins.filter(bin_type='F', in_use=False).count()

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

class BaseStockList(LoginRequiredMixin, ListView):
    """
    Base view for displaying a list of stocks.
    """

    model = Stock
    template_name = 'storehouse/ops/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 10
    queryset = Stock.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_stock'] = self.queryset.filter(deplete=False).count()
        return context

class StockList(BaseStockList):
    """
    Display all products
    """
    paginate_by = 10

class SearchConstructMixin:
    """
    Class that provides search functionality for stocks
    """
    q = 'q'

    def search_construct(self, term):
        stocks = Stock.objects.all().annotate(
            search_vector=SearchVector('sku', 'item__product__product_name')
        ).filter(
            Q(search_vector=term) | Q(item__product__product_name__icontains=term)
        )
        return stocks

class StockSearchView(BaseStockList, SearchConstructMixin):
    """
    Display search results for Supplier.
    """
    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get(self.q)
        deplete = self.request.GET.get('deplete')
        is_placed = self.request.GET.get('is_placed')
        filters = {}
        if deplete:
            filters['deplete'] = True
        if is_placed:
            filters['is_placed'] = False
        if query:
            stocks = self.search_construct(query).filter(**filters)
            context.update({
                'stocks': stocks,
                'query': query
            })
        else:
            stocks = Stock.objects.filter(**filters)
            context.update({
                'stocks': stocks,
            })

        return context

class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = 'storehouse/ops/stock_detail.html'
    context_object_name = 'stock'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class StockCreateUpdate(LoginRequiredMixin):
    template_name = 'storehouse/ops/stock_update.html'
    model = Stock
    form_class = StockForm
    login_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class StockUpdateView(StockCreateUpdate, CreateView):
    context_object_name = 'stock'

    def get_success_url(self):
        return reverse('storehouse:stock-detail', args=[self.object.pk])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        return kwargs
