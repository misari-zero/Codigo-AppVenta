# import json
# import os
#
# from django.conf import settings
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db import transaction
# from django.http import HttpResponse
# from django.http import JsonResponse, HttpResponseRedirect
# from django.template.loader import get_template
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
# from xhtml2pdf import pisa
#
# from core.erp.forms import AlmacenForm
# from core.erp.mixins import ValidatePermissionRequiredMixin
# from core.erp.models import Almacen, Product, DetAlmacen
#
#
# class AlmacenListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
#     model = Almacen
#     template_name = 'almacen/list.html'
#     permission_required = 'erp.view_almacen'
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'searchdata':
#                 data = []
#                 for i in Almacen.objects.all():
#                     data.append(i.toJSON())
#             elif action == 'search_details_prod':
#                 data = []
#                 for i in DetAlmacen.objects.filter(almacen_id=request.POST['id']):
#                     data.append(i.toJSON())
#             else:
#                 data['error'] = 'Ha ocurrido un error'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Listado de Ingreso'
#         context['create_url'] = reverse_lazy('erp:almacen_create')
#         context['list_url'] = reverse_lazy('erp:almacen_list')
#         context['entity'] = 'Almacén'
#         return context
#
#
# class AlmacenCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
#     model = Almacen
#     form_class = AlmacenForm
#     template_name = 'almacen/create.html'
#     success_url = reverse_lazy('erp:almacen_list')
#     permission_required = 'erp.add_almacen'
#     url_redirect = success_url
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'search_products':
#                 data = []
#                 prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
#                 for i in prods:
#                     item = i.toJSON()
#                     # item['value'] = i.name
#                     item['text'] = i.name
#                     data.append(item)
#             elif action == 'add':
#                 with transaction.atomic():
#                     vents = json.loads(request.POST['vents'])
#                     almacen = Almacen()
#                     almacen.sucursal_id = vents('sucursal')
#                     almacen.transf_id = vents('transf')
#                     almacen.doc_id = vents('doc')
#                     almacen.nro= vents('nro')
#                     almacen.date_joined = vents['date_joined']
#                     almacen.subtotal = float(vents['subtotal'])
#                     almacen.igv = float(vents['igv'])
#                     almacen.total = float(vents['total'])
#                     almacen.save()
#                     for i in vents['products']:
#                         det = DetAlmacen()
#                         det.almacen_id = almacen.id
#                         det.prod_id = i['id']
#                         det.cant = int(i['cant'])
#                         det.price = float(i['pvp'])
#                         det.pricecom = float(i['pvpcompra'])
#                         det.total = float(i['total'])
#                         det.save()
#                     data = {'id': almacen.id}
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Creación de un Registro Ingreso'
#         context['entity'] = 'Igresos'
#         context['list_url'] = self.success_url
#         context['action'] = 'add'
#         context['det'] = []
#         return context
#
#
# class AlmacenUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
#     model = Almacen
#     form_class = AlmacenForm
#     template_name = 'almacen/create.html'
#     success_url = reverse_lazy('erp:almacen_list')
#     permission_required = 'erp.change_almacen'
#     url_redirect = success_url
#
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'search_products':
#                 data = []
#                 prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
#                 for i in prods:
#                     item = i.toJSON()
#                     item['value'] = i.name
#                     data.append(item)
#             elif action == 'edit':
#                 with transaction.atomic():
#                     vents = json.loads(request.POST['vents'])
#                     # sale = Sale.objects.get(pk=self.get_object().id)
#                     almacen = self.get_object()
#                     almacen.sucursal_id = vents('sucursal')
#                     almacen.transf_id = vents('tranf')
#                     almacen.doc_id = vents('doc')
#                     almacen.nro = vents('nro')
#                     almacen.date_joined = vents['date_joined']
#                     almacen.subtotal = float(vents['subtotal'])
#                     almacen.iva = float(vents['iva'])
#                     almacen.total = float(vents['total'])
#                     almacen.save()
#                     almacen.detsale_set.all().delete()
#                     for i in vents['products']:
#                         det = DetAlmacen()
#                         det.almacen_id = almacen.id
#                         det.prod_id = i['id']
#                         det.cant = int(i['cant'])
#                         det.price = float(i['pvp'])
#                         det.pricecom = float(i['pvpcompra'])
#                         det.total = float(i['total'])
#                         det.save()
#                     data = {'id': almacen.id}
#             else:
#                 data['error'] = 'No ha ingresado a ninguna opción'
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data, safe=False)
#
#     def get_details_product(self):
#         data = []
#         try:
#             for i in DetAlmacen.objects.filter(almacen_id=self.get_object().id):
#                 item = i.prod.toJSON()
#                 item['cant'] = i.cant
#                 data.append(item)
#         except:
#             pass
#         return data
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Edición de Registro Ingreso'
#         context['entity'] = 'Ingresos'
#         context['list_url'] = self.success_url
#         context['action'] = 'edit'
#         context['det'] = json.dumps(self.get_details_product())
#         return context
#
#
# class AlmacenDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
#     model = Almacen
#     template_name = 'almacen/delete.html'
#     success_url = reverse_lazy('erp:almacen_list')
#     permission_required = 'erp.delete_almacen'
#     url_redirect = success_url
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             self.object.delete()
#         except Exception as e:
#             data['error'] = str(e)
#         return JsonResponse(data)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Eliminación de un Registro'
#         context['entity'] = 'Ingresos'
#         context['list_url'] = self.success_url
#         return context
#
#
# class AlmacenInvoicePdfView(View):
#
#     def link_callback(self, uri, rel):
#         """
#         Convert HTML URIs to absolute system paths so xhtml2pdf can access those
#         resources
#         """
#         # use short variable names
#         sUrl = settings.STATIC_URL  # Typically /static/
#         sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
#         mUrl = settings.MEDIA_URL  # Typically /static/media/
#         mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/
#
#         # convert URIs to absolute system paths
#         if uri.startswith(mUrl):
#             path = os.path.join(mRoot, uri.replace(mUrl, ""))
#         elif uri.startswith(sUrl):
#             path = os.path.join(sRoot, uri.replace(sUrl, ""))
#         else:
#             return uri  # handle absolute uri (ie: http://some.tld/foo.png)
#
#         # make sure that file exists
#         if not os.path.isfile(path):
#             raise Exception(
#                 'media URI must start with %s or %s' % (sUrl, mUrl)
#             )
#         return path
#
#     def get(self, request, *args, **kwargs):
#         try:
#             template = get_template('almacen/invoice.html')
#             context = {
#                 'almacen': Almacen.objects.get(pk=self.kwargs['pk']),
#                 'comp': {'name': 'LA FLORESTA.', 'ruc': '10104222043', 'address': 'Urbanización los ficus Calle Los pétalos 174, Santa Anita'},
#                 'icon': '{}{}'.format(settings.MEDIA_URL, '/logo1.png')
#             }
#             html = template.render(context)
#             response = HttpResponse(content_type='application/pdf')
#             # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
#             pisaStatus = pisa.CreatePDF(
#                 html, dest=response,
#                 link_callback=self.link_callback
#             )
#             return response
#         except:
#             pass
#         return HttpResponseRedirect(reverse_lazy('erp:almacen_list'))
