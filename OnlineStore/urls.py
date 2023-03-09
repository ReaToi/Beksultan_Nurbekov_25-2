"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from products.views import MainPageCVB, ProductCVB, HashtagsCVB, ReviewDetailCVB, CreateProductCVB
from django.conf.urls.static import static
from OnlineStore import settings
from users.views import RegisterCVB, LoginViewCBV, LogoutViewCBV


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', MainPageCVB.as_view(template_name='layouts/index.html')),
    path('products/', ProductCVB.as_view(template_name='products/products.html')),
    path('hashtags/', HashtagsCVB.as_view(template_name='hashtags/hashtags.html')),
    path('products/<int:id>/', ReviewDetailCVB.as_view(template_name='products/detail.html')),
    path('products/create/', CreateProductCVB.as_view(template_name='products/create.html')),

    path('users/register/', RegisterCVB.as_view(template_name='users/register.html')),
    path('users/login/', LoginViewCBV.as_view(template_name='users/login.html')),
    path('users/logout/', LogoutViewCBV.as_view())

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
