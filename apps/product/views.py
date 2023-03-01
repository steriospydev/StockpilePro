from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, Count, Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

import django_filters
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, SubCategory, Product
from .forms import CategoryForm, ProductForm

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
        success_url = reverse('product:product-sublist', args=[subcategory_id])
        return HttpResponseRedirect(success_url)

class ProductCreateView(ProductCreateUpdate, CreateView):
    pass

class ProductUpdateView(ProductCreateUpdate, UpdateView):
    context_object_name = 'product'

class BaseProductList(ListView):
    """
    Base view for displaying a list of products.
    """

    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    queryset = Product.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('package__material', 'subcategory')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = self.queryset.count()
        return context

class ProductList(BaseProductList):
    """
    Display all products
    """
    paginate_by = 10

class SearchConstructMixin:
    q = 'q'
    search_option = 'search_option'

    def search_construct(self, term, option, search_checkboxes):
        lookup = {
            'Ονομα': 'product_name__icontains',
            'Υλικο': 'package__material__material_name__icontains',
            'Υποκατηγορια': 'subcategory__subcategory_name__icontains',
            'SKU': 'sku_num__icontains'
        }
        field_lookup = lookup.get(option, None)
        if field_lookup:
            products = Product.objects.select_related('package__material', 'subcategory').filter(**{field_lookup: term})
        else:
            products = Product.objects.select_related('package__material', 'subcategory').all()

        if 'Available' in search_checkboxes:
            products = products.filter(available=True)

        if 'Online' in search_checkboxes:
            products = products.filter(online_sell=True)

        if 'Active' in search_checkboxes:
            products = products.filter(is_active=True)

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
        search_option = self.request.GET.get(self.search_option)
        search_checkboxes = self.request.GET.getlist('search-check')
        if query:
            products = self.search_construct(query, search_option, search_checkboxes)
            context.update({
                'products': products,
                'query': query,
                'search_option': search_option,
                'search_checkboxes': search_checkboxes,
            })
        return context

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('product:product-list')
    login_url = '/'

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    login_url = '/'
