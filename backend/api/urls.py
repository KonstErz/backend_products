from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SignupView, LoginView, CategoryList,
                    CompanyList, ProductViewSet)


router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('categories/', CategoryList.as_view()),
    path('companies/', CompanyList.as_view()),
]
