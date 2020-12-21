from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoTransForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import TipoTrans


class TipoTransListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TipoTrans
    template_name = 'transferencia/list.html'
    permission_required = 'erp.view_transferencia'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoTrans.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Transferencias'
        context['create_url'] = reverse_lazy('erp:transferencia_create')
        context['list_url'] = reverse_lazy('erp:transferencia_list')
        context['entity'] = 'TipoTransferencias'
        return context


class TipoTransCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TipoTrans
    form_class = TipoTransForm
    template_name = 'transferencia/create.html'
    success_url = reverse_lazy('erp:transferencia_list')
    permission_required = 'erp.add_transferencia'
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
        context['title'] = 'Creación Tipo Transferencia'
        context['entity'] = 'TipoTranferencias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoTransUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TipoTrans
    form_class = TipoTransForm
    template_name = 'transferencia/create.html'
    success_url = reverse_lazy('erp:transferencia_list')
    permission_required = 'erp.change_transferencia'
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
        context['title'] = 'Edición un Tipo Transferencia'
        context['entity'] = 'TipoTransferencias'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoTransDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TipoTrans
    template_name = 'transferencia/delete.html'
    success_url = reverse_lazy('erp:transferencia_list')
    permission_required = 'erp.delete_transferencia'
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
        context['title'] = 'Eliminación de un Tipo Transferencia'
        context['entity'] = 'TipoTransferencia'
        context['list_url'] = self.success_url
        return context
