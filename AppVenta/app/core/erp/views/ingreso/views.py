from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import IngresoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Ingreso


class IngresoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Ingreso
    template_name = 'ingreso/list.html'
    permission_required = 'erp.view_ingreso'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ingreso.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de Ingresos'
        context['create_url'] = reverse_lazy('erp:ingreso_create')
        context['list_url'] = reverse_lazy('erp:ingreso_list')
        context['entity'] = 'Ingresos'
        return context


class IngresoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'ingreso/create.html'
    success_url = reverse_lazy('erp:ingreso_list')
    permission_required = 'erp.add_ingreso'
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
        context['title'] = 'Creación Registro Ingreso'
        context['entity'] = 'Ingresos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class IngresoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ingreso
    form_class = IngresoForm
    template_name = 'ingreso/create.html'
    success_url = reverse_lazy('erp:ingreso_list')
    permission_required = 'erp.change_ingreso'
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
        context['title'] = 'Edición Registro Ingresos'
        context['entity'] = 'Ingresos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class IngresoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Ingreso
    template_name = 'ingreso/delete.html'
    success_url = reverse_lazy('erp:ingreso_list')
    permission_required = 'erp.delete_ingreso'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación  Registro Ingresos'
        context['entity'] = 'Ingresos'
        context['list_url'] = self.success_url
        return context
