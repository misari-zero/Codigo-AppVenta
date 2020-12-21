from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import TipoDocForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import TipoDoc


class TipoDocListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TipoDoc
    template_name = 'documento/list.html'
    permission_required = 'erp.view_documento'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoDoc.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Documentos'
        context['create_url'] = reverse_lazy('erp:documento_create')
        context['list_url'] = reverse_lazy('erp:documento_list')
        context['entity'] = 'TipoDocumentos'
        return context


class TipoDocCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TipoDoc
    form_class = TipoDocForm
    template_name = 'documento/create.html'
    success_url = reverse_lazy('erp:documento_list')
    permission_required = 'erp.add_documento'
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
        context['title'] = 'Creación de documento'
        context['entity'] = 'TipoDocumentos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoDocUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TipoDoc
    form_class = TipoDocForm
    template_name = 'documento/create.html'
    success_url = reverse_lazy('erp:documento_list')
    permission_required = 'erp.change_documento'
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
        context['title'] = 'Edición de documento'
        context['entity'] = 'TipoDocumentos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoDocDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TipoDoc
    template_name = 'documento/delete.html'
    success_url = reverse_lazy('erp:documento_list')
    permission_required = 'erp.delete_documento'
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
        context['title'] = 'Eliminación de un Documento'
        context['entity'] = 'TipoDocumentos'
        context['list_url'] = self.success_url
        return context
