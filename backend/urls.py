from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

# from .views import domain_list, domain_detail

# urlpatterns = [
#     path('api/domains/', domain_list, name='Domain List'),
#     path('api/domains/<str:pk>', domain_detail, name='Domain Detail')
# ]

router = DefaultRouter()
router.register(r'domains', views.DomainViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]


