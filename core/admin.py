from django.contrib import admin
from .models import Categoria, Producto, Cliente, Venta, DetalleVenta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'talla', 'color', 'stock', 'activo')
    list_filter = ('categoria', 'talla', 'color', 'activo')
    search_fields = ('nombre', 'color')
    list_editable = ('precio', 'stock', 'activo')


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha', 'estado', 'total')
    list_filter = ('estado', 'fecha')
    inlines = [DetalleVentaInline]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'dni', 'email', 'telefono')
    search_fields = ('nombre', 'dni')
