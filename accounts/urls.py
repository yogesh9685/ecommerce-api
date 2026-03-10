from django.urls import path , include
from .views import RegisterView, ProfileView ,LoginView ,OtpView ,home , cart,  seller ,  addProduct , ProductListView , CategoryListView ,  logout_view , seller
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', CategoryListView)
router.register('products', ProductListView)

urlpatterns = [

    path("register/", RegisterView.as_view()),

    path("login/", LoginView.as_view()),

    path("profile/", ProfileView.as_view()),

    path("otp/", OtpView.as_view()),

    path("home/", home),

    path("", include(router.urls)),   # router urls
    
    path('logout/' , logout_view),

    path('add/' , addProduct),

    path('seller/' , seller),

    path("cart/" , cart),
] 