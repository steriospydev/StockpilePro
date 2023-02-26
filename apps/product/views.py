from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Sum, Count

from .models import Category, SubCategory
# Create your views here.


class CategoryListView(ListView):
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

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_queryset(self):
        return Category.objects.prefetch_related('subs__sub_products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        subcategories = category.subs.annotate(num_products=Count('sub_products'))
        context['subcategories'] = subcategories
        context['num_products'] = sum(subcategory.num_products for subcategory in subcategories)
        return context
