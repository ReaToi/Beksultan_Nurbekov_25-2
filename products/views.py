from django.shortcuts import render
from products.models import Product, Hashtag


# Create your views here.


def main_page_vief(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {
            'products':
                [
                    {
                        'id': product.id,
                        'title': product.title,
                        'rate': product.rate,
                        'image': product.image,
                        'hashtags': product.hashtags.all(),
                    }
                    for product in products
                ]
        }
        return render(request, 'products/products.html', context=context)


def hashtags(request):

    if request.method == 'GET':
        hashtags = Hashtag.objects.all()
        context = {
            'hashtags': hashtags
        }
        return render(request, 'hashtags/hashtags.html', context=context)









