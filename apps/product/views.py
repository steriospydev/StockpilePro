from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)

from django.db.models import Count, Prefetch, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramSimilarity


from .models import (Category, SubCategory, Product, Tax, Package, Material)
from .forms import (CategoryForm, ProductForm, SubCategoryForm,
                    TaxForm, PackageForm, MaterialForm, SubCategoryFullForm)
from ..invoice.models import InvoiceItem

def get_invoice_report(product):
    invoice_items = InvoiceItem.objects.filter(product=product)

    # calculate total quantity, total taxes, and total value
    total_quantity = invoice_items.aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_taxes = invoice_items.aggregate(Sum('total_tax'))['total_tax__sum'] or 0
    total_value = invoice_items.aggregate(Sum('line_subtotal'))['line_subtotal__sum'] or 0

    # count the number of invoices
    no_of_invoices = invoice_items.values('invoice').distinct().count()

    # return the calculated values
    return {
        'total_quantity': total_quantity,
        'total_taxes': total_taxes,
        'total_value': total_value,
        'no_of_invoices': no_of_invoices,
    }
# Category based views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'product/category/category_list.html'

    def get_queryset(self):
        return Category.objects.prefetch_related('subs__sub_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = self.get_queryset()
        for category in categories:
            category.num_products = category.get_num_products()
        context['categories'] = categories
        context['num_products'] = sum(category.num_products for category in categories)
        return context

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'product/category/category_detail.html'

    def get_queryset(self):
        return Category.objects.prefetch_related('subs__sub_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        subcategories = category.subs.annotate(
            num_products=Count('sub_products')).order_by('subcategory_name')
        context['subcategories'] = subcategories
        context['num_products'] = sum(subcategory.num_products for subcategory in subcategories)
        return context

class CategoryCreateUpdate(LoginRequiredMixin):
    template_name = 'product/category/category_create_update.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('product:category-list')
    login_url = '/'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CategoryCreateView(CategoryCreateUpdate, CreateView):
    pass

class CategoryUpdateView(CategoryCreateUpdate, UpdateView):
    context_object_name = 'category'

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'product/category/category_confirm_delete.html'
    success_url = reverse_lazy('product:category-list')
    login_url = '/'

class SubCategoryCreateUpdate(LoginRequiredMixin):
    template_name = 'product/category/subcategory_create.html'
    model = SubCategory
    form_class = SubCategoryForm
    login_url = '/'

    def get_success_url(self):
        return reverse_lazy('product:category-detail', kwargs={'pk': self.kwargs['category_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['category_id'])
        context['category'] = category
        return context

    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_id']
        return super().form_valid(form)

class SubCategoryCreateView(SubCategoryCreateUpdate, CreateView):
    pass

class SubCategoryUpdateView(SubCategoryCreateUpdate, UpdateView):
    pass

class SubProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/category/sub_products.html'

    def get_queryset(self):
        # Fetch the SubCategory object and
        # prefetch its related products and
        # category in a single query
        queryset = SubCategory.objects.prefetch_related(
            Prefetch('sub_products', queryset=Product.objects.annotate(num_products=Count('id')))
        ).select_related('category').get(pk=self.kwargs['pk']).sub_products.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = SubCategory.objects.select_related('category').get(pk=self.kwargs['pk'])
        context['subcategory'] = subcategory
        context['num_products'] = context['object_list'].aggregate(num_products=Count('id'))['num_products']
        context['category'] = subcategory.category
        return context

# Product based views
class ProductCreateUpdate(LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create_update.html'
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        subcategory_id = form.cleaned_data['subcategory'].id
        self.object.save()
        success_url = reverse('product:product-detail', args=[self.object.pk])
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ProductCreateView(ProductCreateUpdate, CreateView):
    pass

class ProductUpdateView(ProductCreateUpdate, UpdateView):
    context_object_name = 'product'

class BaseProductList(LoginRequiredMixin, ListView):
    """
    Base view for displaying a list of products.
    """

    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('package__material', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = self.queryset.count()
        return context

class SearchConstructMixin:
    """
    Class that provides search functionality for products
    """
    q = 'q'

    def search_construct(self, term):
        products = Product.objects.select_related('package__material', 'subcategory').annotate(
            similarity=TrigramSimilarity('product_name', term)
        ).filter(similarity__gt=0.1).order_by('-similarity')
        return products

class ProductSearchView(BaseProductList, SearchConstructMixin):
    """
    Display search results for Supplier.
    """
    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get(self.q)
        available = self.request.GET.get('available')
        active = self.request.GET.get('active')
        online = self.request.GET.get('online')
        filters = {}
        if available:
            filters['available'] = False
        if active:
            filters['is_active'] = False
        if online:
            filters['online_sell'] = True
        if query:
            products = self.search_construct(query).filter(**filters)
            context.update({
                'products': products,
                'query': query
            })
        else:
            products = Product.objects.filter(**filters)
            context.update({
                'products': products,
            })

        return context

class ProductList(BaseProductList):
    """
    Display all products
    """
    paginate_by = 10

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:product-list')
    login_url = '/'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['invoice_report'] = get_invoice_report(product)
        return context


class TaxCreateView(LoginRequiredMixin, CreateView):
    model = Tax
    form_class = TaxForm
    template_name = 'product/misc_product/tax_create.html'
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        success_url = reverse('product:product-create')
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SubFullCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryFullForm
    template_name = 'product/misc_product/subcategory_create.html'
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        success_url = reverse('product:product-create')
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PackageCreateView(LoginRequiredMixin, CreateView):
    model = Package
    form_class = PackageForm
    template_name = 'product/misc_product/package_create.html'
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        success_url = reverse('product:product-create')
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class MaterialCreateView(LoginRequiredMixin, CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'product/misc_product/material_create.html'
    login_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        success_url = reverse('product:package-create')
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
