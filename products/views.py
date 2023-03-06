from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT

# Create your views here.


def main_page_vief(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('-create_date')
        # products = Product.objects.all().order_by('-rate')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page + 1)
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page-1):PAGINATION_LIMIT * page]

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
                'user': request.user,
                'pages': range(1, max_page+1),

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






