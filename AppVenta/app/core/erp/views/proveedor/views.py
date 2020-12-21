from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import ProveedorForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Proveedor


class ProveedorListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Proveedor
    template_name = 'proveedor/list.html'
    permission_required = 'erp.view_proveedor'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Proveedor.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('erp:proveedor_create')
        context['list_url'] = reverse_lazy('erp:proveedor_list')
        context['entity'] = 'Proveedores'
        return context


class ProveedorCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/create.html'
    success_url = reverse_lazy('erp:proveedor_list')
    permission_required = 'erp.add_proveedor'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ProveedorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/create.html'
    success_url = reverse_lazy('erp:proveedor_list')
    permission_required = 'erp.change_proveedor'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ProveedorDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'proveedor/delete.html'
    success_url = reverse_lazy('erp:proveedor_list')
    permission_required = 'erp.delete_proveedor'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Proveedor'
        context['entity'] = 'Proveedores'
        context['list_url'] = self.success_url
        return context
