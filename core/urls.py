from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoriaViewSet, ProductoViewSet, ClienteViewSet,
    VentaViewSet, crear_venta
)

router = DefaultRouter()
router.register('categorias', CategoriaViewSet)
router.register('productos', ProductoViewSet)
router.register('clientes', ClienteViewSet)
router.register('ventas', VentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('crear-venta/', crear_venta, name='crear_venta'),
]