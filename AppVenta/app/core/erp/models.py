from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from app.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel
from django.db.models import signals


class Category(BaseModel):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')
    pvpcompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de compra')
    stock = models.PositiveSmallIntegerField()
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        item['pvpcompra'] = format(self.pvpcompra, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']


class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    # def get_full_name(self):
    #     return '{} {} / {}'.format(self.names, self.surnames, self.dni)

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']


class Proveedor(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    empresa = models.CharField(max_length=150, verbose_name='Empresa')
    telefono = models.IntegerField()
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    igv = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

def update_stock(sender, instance, **kwargs):
    instance.prod.stock -= instance.cant
    instance.prod.save()

# register the signa
signals.post_save.connect(update_stock, sender=DetSale, dispatch_uid="update_stock_count")


class Sucursal(models.Model):
    name = models.CharField(max_length=150, verbose_name='Sucursal')
    direccion = models.CharField(max_length=150, verbose_name='Dirección')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['id']


class TipoTrans(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre Tipo Transferencia')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoTransferencia'
        verbose_name_plural = 'TipoTransferencias'
        ordering = ['id']


class TipoDoc(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre Tipo Documento')
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'TipoDocumento'
        verbose_name_plural = 'TipoDocumentos'
        ordering = ['id']


class Almacen(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    transf = models.ForeignKey(TipoTrans, on_delete=models.CASCADE)
    doc = models.ForeignKey(TipoDoc, on_delete=models.CASCADE)
    nro = models.IntegerField()
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    igv = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.sucursal.name

    def toJSON(self):
        item = model_to_dict(self)
        item['sucursal'] = self.sucursal.toJSON()
        item['transf'] = self.transf.toJSON()
        item['doc'] = self.doc.toJSON()
        item['nro'] = self.nro.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detalmacen_set.all()]
        return item

    # def generte_nro(self):
    #     return 'E{}-{}'.format(format(self.id, '03d'), format(self.id, '06d'))

    class Meta:
        verbose_name = 'Almacen'
        verbose_name_plural = 'Almacenes'
        ordering = ['id']


# def generte_nro(self):
#     return 'E{}-{}'.format(format(self.id, '03d'), format(self.id, '06d'))

class DetAlmacen(models.Model):
    almacen = models.ForeignKey(Almacen, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    pricecom = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['almacen'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['pricecom'] = format(self.pricecom, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Ingreso'
        verbose_name_plural = 'Detalle de Ingresos'
        ordering = ['id']

def update_stock(sender, instance, **kwargs):
	instance.prod.stock += instance.cant
	instance.prod.save()

# register the signal
signals.post_save.connect(update_stock, sender=DetAlmacen, dispatch_uid="update_stock_count")


class Ingreso(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default="<pk:1>")
    transf = models.ForeignKey(TipoTrans, on_delete=models.CASCADE,default="INGRESO POR COMPRAS", verbose_name='Tipo Transferencia')
    doc = models.ForeignKey(TipoDoc, on_delete=models.CASCADE, verbose_name='Tipo documento')
    nro = models.IntegerField(verbose_name='Nro Documento')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Registro')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    pricecompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Compra')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    igv = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IGV')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.sucursal.name

    def toJSON(self):
        item = model_to_dict(self)
        item['sucursal'] = self.sucursal.toJSON()
        item['transf'] = self.transf.toJSON()
        item['doc'] = self.doc.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['cat'] = self.cat.toJSON()
        item['prod'] = self.prod.toJSON()
        item['pricecompra'] = format(self.pricecompra, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['id']

# def update_preciocompra(sender, instance, **kwargs):
# 	instance.prod.pvpcompra == instance.pricecompra
# 	instance.prod.save()
#
# # register the signal
# signals.post_save.connect(update_preciocompra, sender=Ingreso, dispatch_uid="update_preciocompra_count")

def update_stock(sender, instance, **kwargs):
    instance.prod.stock += instance.cant
    instance.prod.save()

# register the signal
signals.post_save.connect(update_stock, sender=Ingreso, dispatch_uid="update_stock_count")



class Salida(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default="<pk:1>")
    transf = models.ForeignKey(TipoTrans, on_delete=models.CASCADE, verbose_name='Tipo Transferencia')
    doc = models.ForeignKey(TipoDoc, on_delete=models.CASCADE, verbose_name='Tipo documento')
    nro = models.IntegerField(verbose_name='Nro Documento')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha Registro')
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    prod = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    pricecompra = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de Compra')
    cant = models.IntegerField(default=0, verbose_name='Cantidad')
    igv = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='IGV')
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.sucursal.name

    def toJSON(self):
        item = model_to_dict(self)
        item['sucursal'] = self.sucursal.toJSON()
        item['transf'] = self.transf.toJSON()
        item['doc'] = self.doc.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['cat'] = self.cat.toJSON()
        item['prod'] = self.prod.toJSON()
        item['pricecompra'] = format(self.pricecompra, '.2f')
        item['igv'] = format(self.igv, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ['id']

# def update_preciocompra(sender, instance, **kwargs):
# 	instance.prod.pvpcompra == instance.pricecompra
# 	instance.prod.save()
#
# # register the signal
# signals.post_save.connect(update_preciocompra, sender=Ingreso, dispatch_uid="update_preciocompra_count")

