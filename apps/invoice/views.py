from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count

from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemForm

class BaseInvoiceList(LoginRequiredMixin, ListView):
    """
    Base view for displaying a list of invoices.
    """

    model = Invoice
    template_name = 'invoice/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 10
    queryset = Invoice.objects.annotate(num_items=Count('id')).select_related('supplier')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_invoices'] = self.queryset.count()
        return context

class InvoiceList(BaseInvoiceList):
    """
    Display all products
    """
    paginate_by = 10

class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoice/invoice_detail.html'
    context_object_name = 'invoice'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = self.object # the current invoice object
        invoice_items = invoice.invoice_items.select_related('product').select_related(
            'product__package').select_related('product__package__material')
        context['invoice_items'] = invoice_items
        return context


@login_required(login_url='/')
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.created_by = request.user
            invoice.save()
            return redirect('invoice:invoice-list')
    else:
        form = InvoiceForm()
    return render(request, 'invoice/invoice_create.html', {'form': form})

@login_required(login_url='/')
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})
