from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from django.core.paginator import Paginator
from django import forms


def home(request):
    # Выбираем 5 последних продуктов
    latest_products = Product.objects.order_by('-id')[:5]

    # Выводим их в консоль
    print('Вывод 5 последних продуктов:')
    for product in latest_products:
        print(f"id: {product.id}, Название: {product.name}, цена за покупку: {product.price}")

    return render(request, 'catalog/home.html', {'products': latest_products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        message = request.POST.get('message')
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
    return render(request, 'catalog/contacts.html')


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_detail.html', context=context)


def products_list(requests):
    products = Product.objects.all()

    paginator = Paginator(products, 2)
    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'page_obj': page_obj,
    }
    return render(requests, 'catalog/products_list.html', context=context)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']


def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('/')
    return render(request, 'catalog/add_product.html', {'form': form})
