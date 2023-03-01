from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Review
from products.forms import ProductCreateForm, ReviewCreateForm

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
                ],
                'user': request.user
        }
        return render(request, 'products/products.html', context=context)


def hashtags(request):
    if request.method == 'GET':
        hashtags = Hashtag.objects.all()
        context = {
            'hashtags': hashtags
        }
        return render(request, 'hashtags/hashtags.html', context=context)


def review_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'comments': product.Review.all(),
            'form': ReviewCreateForm
        }
        return render(request, 'products/detail.html', context=context)

    if request.method == 'POST':
        data = request.POST
        form = ReviewCreateForm(data=data)
        product = Product.objects.get(id=id)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product=product,
            )
            context = {
                'product': product,
                'comments': product.Review.all(),
                'form': ReviewCreateForm
            }
        return render(request, 'products/detail.html', context=context)


def create_product_view(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        data, files = request.POST, request.FILES

        form = ProductCreateForm(data, files)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate'),
            )
            return redirect('/products')
        return render(request, 'products/create.html', context={
            'form': form
        })






