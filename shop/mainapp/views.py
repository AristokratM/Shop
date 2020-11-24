from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Notebook, Smartphone, Category
from .mixins import CategoryDetailMixin

# Create your views here.


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.object.get_categories_for_left_sidebar()
        return render(request, 'shop/base.html', {'categories': categories})


class ProductDetailView(CategoryDetailMixin, DetailView):
    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs.get('ct_model')]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.object.all()
    context_object_name = 'category'
    template_name = 'shop/category_detail.html'
    slug_url_kwarg = 'slug'
