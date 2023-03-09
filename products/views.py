from django.shortcuts import render, redirect
from products.models import Product, Hashtag, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView, DeleteView


# Create your views here.


class MainPageCVB(ListView):
    model = Product


class ProductCVB(ListView):
    model = Product

    def get(self, request, *args, **kwargs):
        products = self.get_queryset().order_by('-create_date')
        # products = self.get_queryset().order_by('-rate')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__contains=search) | products.filter(description__contains=search)

        max_page = products.__len__() / PAGINATION_LIMIT

        if round(max_page) < max_page:
            max_page = round(max_page + 1)
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

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
            'pages': range(1, max_page + 1),

        }
        return render(request, self.template_name, context=context)


class HashtagsCVB(ListView):
    model = Hashtag

    def get(self, request, *args, **kwargs):
        hashtags = self.get_queryset()
        context = {
            'hashtags': hashtags
        }
        return render(request, self.template_name, context=context)


class ReviewDetailCVB(ListView, CreateView):

    def get(self, request, id, *args, **kwargs):
        product = Product.objects.get(id=id)
        # product = self.get(id=id)
        context = {
            'product': product,
            'comments': Review.objects.all(),
            'form': ReviewCreateForm
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = ReviewCreateForm(data=data)
        product = self.model

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
        return render(request, self.template_name, context=context)


class CreateProductCVB(ListView, CreateView):
    model = Product
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': self.form_class if not kwargs.get('form') else kwargs['form']
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):

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
        return render(request, self.template_name, context={
            'form': form
        })
