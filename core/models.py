from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


class Producto(models.Model):
    TALLAS = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'),
        ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'),
    ]

    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    talla = models.CharField(max_length=5, choices=TALLAS, default='M')
    color = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.talla})"

    @property
    def tiene_descuento(self):
        return self.precio_original and self.precio_original > self.precio


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.dni}"


class Venta(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('enviada', 'Enviada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]

    METODOS_PAGO = [
        ('yape', 'Yape'),
        ('plin', 'Plin'),
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('transferencia', 'Transferencia bancaria'),
        ('contraentrega', 'Pago contra entrega'),
    ]

    TIPOS_ENVIO = [
        ('recojo', 'Recojo en tienda (gratis)'),
        ('delivery_lima', 'Delivery Lima (S/ 10.00)'),
        ('delivery_provincia', 'Delivery Provincia (S/ 20.00)'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    # NUEVOS CAMPOS
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='yape')
    tipo_envio = models.CharField(max_length=20, choices=TIPOS_ENVIO, default='recojo')
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente.nombre}"
    
    def calcular_total(self):
        self.subtotal = sum(item.subtotal() for item in self.items.all())
        self.total = self.subtotal + self.costo_envio
        self.save()
        return self.total
    
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"