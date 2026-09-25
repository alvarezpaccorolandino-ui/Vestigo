from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Categoria, Producto, Cliente, Venta, DetalleVenta
from .serializers import (
    CategoriaSerializer, ProductoSerializer, ClienteSerializer,
    VentaSerializer, DetalleVentaSerializer
)


# ---------- VISTAS DE LA WEB ----------
def catalogo(request):
    """Muestra la página del catálogo de ropa."""
    return render(request, 'catalogo.html')


# ---------- API REST ----------
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.filter(activo=True)
    serializer_class = ProductoSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('-fecha')
    serializer_class = VentaSerializer


@api_view(['POST'])
def crear_venta(request):
    """
    Recibe: { cliente_id, items: [{producto_id, cantidad}] }
    Crea la venta, descuenta stock y calcula total.
    """
    data = request.data
    cliente = get_object_or_404(Cliente, id=data['cliente_id'])

    venta = Venta.objects.create(cliente=cliente, estado='pendiente')

    for item in data['items']:
        producto = get_object_or_404(Producto, id=item['producto_id'])
        cantidad = item['cantidad']

        if producto.stock < cantidad:
            return Response(
                {'error': f'Stock insuficiente para {producto.nombre}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        DetalleVenta.objects.create(
            venta=venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )

        producto.stock -= cantidad
        producto.save()

    venta.calcular_total()
    return Response(VentaSerializer(venta).data, status=status.HTTP_201_CREATED)
