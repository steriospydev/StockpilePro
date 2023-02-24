from django.shortcuts import render

from .models import Category
# Create your views here.
def category_view(request):
    categories = Category.objects.all()

    return render(request, 'product/category_list.html',
                  {'categories': categories})
