from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Sum, Count, Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Category, SubCategory, Product
from .forms import CategoryForm
# Create your views here.


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'

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
    template_name = 'product/category_detail.html'

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

class SubProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product/sub_products.html'

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


class CategoryCreateUpdate(LoginRequiredMixin):
    template_name = 'product/category_create_update.html'
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
    success_url = reverse_lazy('product:category-list')
    login_url = '/'
