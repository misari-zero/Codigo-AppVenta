from django.urls import path
#
# from core.erp.views.almacen.views import AlmacenListView, AlmacenCreateView, AlmacenDeleteView, AlmacenUpdateView, \
#     AlmacenInvoicePdfView
from core.erp.views.category.views import *
from core.erp.views.client.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.documento.views import TipoDocListView, TipoDocCreateView, TipoDocUpdateView, TipoDocDeleteView
from core.erp.views.ingreso.views import IngresoListView, IngresoCreateView, IngresoDeleteView, IngresoUpdateView
from core.erp.views.product.views import *
from core.erp.views.proveedor.views import ProveedorListView, ProveedorCreateView, ProveedorUpdateView, \
    ProveedorDeleteView
from core.erp.views.sale.views import SaleCreateView, SaleListView, SaleDeleteView, SaleUpdateView, SaleInvoicePdfView
from core.erp.views.salida.views import SalidaListView, SalidaCreateView, SalidaDeleteView, SalidaUpdateView
from core.erp.views.sucursal.views import SucursalListView, SucursalCreateView, SucursalUpdateView, SucursalDeleteView
from core.erp.views.tests.views import TestView
from core.erp.views.transferencia.views import TipoTransListView, TipoTransCreateView, TipoTransUpdateView, \
    TipoTransDeleteView

app_name = 'erp'

urlpatterns = [
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # client
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # proveedor
    path('proveedor/list/', ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedor/add/', ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedor/update/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedor/delete/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_delete'),
    # product
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    # sucursal
    path('sucursal/list/', SucursalListView.as_view(), name='sucursal_list'),
    path('sucursal/add/', SucursalCreateView.as_view(), name='sucursal_create'),
    path('sucursal/update/<int:pk>/', SucursalUpdateView.as_view(), name='sucursal_update'),
    path('sucursal/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),
    # transferencia
    path('transferencia/list/', TipoTransListView.as_view(), name='transferencia_list'),
    path('transferencia/add/', TipoTransCreateView.as_view(), name='transferencia_create'),
    path('transferencia/update/<int:pk>/', TipoTransUpdateView.as_view(), name='transferencia_update'),
    path('transferencia/delete/<int:pk>/', TipoTransDeleteView.as_view(), name='transferencia_delete'),
    # documento
    path('documento/list/', TipoDocListView.as_view(), name='documento_list'),
    path('documento/add/', TipoDocCreateView.as_view(), name='documento_create'),
    path('documento/update/<int:pk>/', TipoDocUpdateView.as_view(), name='documento_update'),
    path('documento/delete/<int:pk>/', TipoDocDeleteView.as_view(), name='documento_delete'),
    # almacen
    # path('almacen/list/', AlmacenListView.as_view(), name='almacen_list'),
    # path('almacen/add/', AlmacenCreateView.as_view(), name='almacen_create'),
    # path('almacen/delete/<int:pk>/', AlmacenDeleteView.as_view(), name='almacen_delete'),
    # path('almacen/update/<int:pk>/', AlmacenUpdateView.as_view(), name='almacen_update'),
    # path('almacen/invoice/pdf/<int:pk>/', AlmacenInvoicePdfView.as_view(), name='almacen_invoice_pdf'),
    # ingreso
    path('ingreso/list/', IngresoListView.as_view(), name='ingreso_list'),
    path('ingreso/add/', IngresoCreateView.as_view(), name='ingreso_create'),
    path('ingreso/delete/<int:pk>/', IngresoDeleteView.as_view(), name='ingreso_delete'),
    path('ingreso/update/<int:pk>/', IngresoUpdateView.as_view(), name='ingreso_update'),
    # path('ingreso/invoice/pdf/<int:pk>/', IngresoInvoicePdfView.as_view(), name='ingreso_invoice_pdf'),
    # salida
    path('salida/list/', SalidaListView.as_view(), name='salida_list'),
    path('salida/add/', SalidaCreateView.as_view(), name='salida_create'),
    path('salida/delete/<int:pk>/', SalidaDeleteView.as_view(), name='salida_delete'),
    path('salida/update/<int:pk>/', SalidaUpdateView.as_view(), name='salida_update'),
    # path('ingreso/invoice/pdf/<int:pk>/', IngresoInvoicePdfView.as_view(), name='ingreso_invoice_pdf'),
]
