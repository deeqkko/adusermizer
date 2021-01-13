from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views


router = DefaultRouter()
router.register(r'domains', views.DomainViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'ou', views.OrganizationalUnitViewSet)
router.register(r'domainusers', views.DomainUserViewSet)
router.register(r'domaingroups', views.DomainGroupViewSet)
router.register(r'domainou', views.DomainOrganizationalUnitViewSet)

urlpatterns = [
    path('api', include(router.urls))
]


