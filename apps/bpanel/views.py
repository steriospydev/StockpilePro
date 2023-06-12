from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import F, Sum, Value, CharField
from django.db.models.functions import TruncMonth, Concat
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .forms import DTaskForm, ProductChartForm
from .models import DTask
from ..invoice.models import Invoice, InvoiceItem
from ..product.models import Product
from ..supplier.models import Supplier
from ..storehouse.models import Storage, Stock

from .graphs.invoice_reports import construct_overall, construct_month_total_chart
from .graphs.product_reports import construct_product_chart


@login_required
def index(request):
    # Count objects
    num_storages = Storage.objects.count()
    num_products = Product.objects.count()
    num_invoices = Invoice.objects.count()
    num_suppliers = Supplier.objects.count()
    if request.method == 'POST':
        form = DTaskForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.username = request.user
            todo.save()
            return redirect('bpanel:index')
    else:
        form = DTaskForm(initial={'username': request.user})
    todos = DTask.objects.filter(username=request.user) or None
    context = {'form': form, 'todos': todos,
               'num_storages': num_storages,
               'num_products': num_products,
               'num_invoices': num_invoices,
               'num_suppliers': num_suppliers}
    return render(request, 'bpanel/index.html', context)

def remove(request, item_id):
    item = DTask.objects.get(id=item_id)
    item.delete()
    return redirect('bpanel:index')

def change_status(request, item_id):
    item = DTask.objects.get(id=item_id)
    if item.completed:
        item.completed = False
    else:
        item.completed = True
    item.save()
    return redirect('bpanel:index')

@login_required
def ops_report(request):
    product_sold = Stock.objects.aggregate(Sum('retrieved'))['retrieved__sum'] or 0
    supplier_info = Invoice.objects.values('supplier__company').annotate(subtotal=Sum('subtotal'),
                                                                         total_taxes=Sum('total_taxes'))
    product_in_storages = Stock.objects.aggregate(total=Sum('start_quantity') - Sum('retrieved'))['total'] or 0
    most_retrieved_product = Stock.objects.values('item__product__product_name').annotate(total_item_sold=Sum(
        'retrieved')).order_by('-total_item_sold')[:5]

    context = {
        'product_sold': product_sold,
        'supplier_info': supplier_info,
        'product_in_storages': product_in_storages,
        'most_retrieved_product': most_retrieved_product}
    return render(request, 'bpanel/report.html', context)

@login_required
def invoice_chart(request):
    # Aggregate the total for each month using Django ORM
    invoice_data = Invoice.objects.annotate(
        month=TruncMonth('date_of_issuance')).values('month').annotate(total=Sum('total')).order_by('month')
    print(type(invoice_data))
    # Get a list of all years in the data
    years = list(set([d['month'].year for d in invoice_data]))

    # Generate a chart for each year
    charts = {}
    for year in sorted(years, reverse=True):
        charts[year] = construct_month_total_chart(invoice_data, year)

    overall_chart = construct_overall(invoice_data)

    context = {'charts': charts, 'overall_chart_or_none': overall_chart}
    return render(request, 'bpanel/invoice_chart.html', context)

@login_required
def product_report(request):
    context = {}

    stock_aggregate = Stock.objects.values('item__product').annotate(
        product_name=F('item__product__product_name'),
        package_str=Concat(
            F('item__product__package__package_quantity'),
            F('item__product__package__package_unit'),
            Value(' '),
            F('item__product__package__material__material_name'),
            output_field=CharField(),
        ),
        total_bought=Sum('start_quantity'),
        total_sold=Sum('retrieved'),
        total_available=Sum('start_quantity') - Sum('retrieved')
    )

    form = ProductChartForm()
    if request.method == 'POST':
        form = ProductChartForm(request.POST)
        if form.is_valid():
            # Retrieve product value from the form
            get_product = form.cleaned_data['product']
            context['get_product'] = str(Product.objects.get(id=get_product))
            # Filter the stock aggregate by the selected product
            product = stock_aggregate.filter(item__product=get_product)
            if product:
                chart = construct_product_chart(product)
                context['product'] = product
                context['chart'] = chart
            context['product'] = product or None
    context['stock_aggregate'] = stock_aggregate
    context['form'] = form

    return render(request, 'bpanel/product_chart.html', context)
