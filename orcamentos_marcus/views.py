# -*- coding: utf-8 -*-

from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages

from orcamentos_marcus.forms import (
    FormWall,
    FormTypePaint,
    FormRoom,
    FormBudget
)
from orcamentos_marcus.models import (
    TypePaint,
    TypeWall,
    Room,
    Customer,
    Budget
)


class DeleteBudget(DeleteView):
    template_name = 'orcamento_marcus/delete_budget.html'
    model = Budget
    http_method_names = ['post', ]
    success_url = reverse_lazy('list_budget')

    def get_success_url(self):
        messages.success(self.request, _(u'Orcamento deletado com sucesso'))
        return super(DeleteBudget, self).get_success_url()


class DeleteCustomer(DeleteView):
    template_name = 'orcamento_marcus/delete_customer.html'
    model = Customer
    http_method_names = ['post', ]
    success_url = reverse_lazy('list_customer')

    def get_success_url(self):
        messages.success(self.request, _(u'Cliente deletado com sucesso'))
        return super(DeleteCustomer, self).get_success_url()


class DeleteTypePaint(DeleteView):
    template_name = 'orcamento_marcus/delete_type_paint.html'
    model = TypePaint
    http_method_names = ['post', ]
    success_url = reverse_lazy('list_type_paint')

    def get_success_url(self):
        messages.success(self.request, _(u'Tipo de pintura deletado com sucesso'))
        return super(DeleteTypePaint, self).get_success_url()


class DeleteRoom(DeleteView):
    template_name = 'orcamento_marcus/delete_room.html'
    model = Room
    http_method_names = ['post', ]
    success_url = reverse_lazy('list_room')

    def get_success_url(self):
        messages.success(self.request, _(u'Comodo deletado com sucesso'))
        return super(DeleteRoom, self).get_success_url()


class DeleteWall(DeleteView):
    template_name = 'orcamento_marcus/delete_wall.html'
    model = TypeWall
    http_method_names = ['post', ]
    success_url = reverse_lazy('list_wall')

    def get_success_url(self):
        messages.success(self.request, _(u'Parede deletada com sucesso'))
        return super(DeleteWall, self).get_success_url()


class UpdateBudget(UpdateView):
    template_name = 'orcamento_marcus/update_budget.html'
    model = Budget
    success_url = reverse_lazy('list_budget')

    def form_valid(self, form):
        messages.success(self.request, _(u'Orcamento alterado com sucesso!'))
        return super(UpdateBudget, self).form_valid(form)


class UpdateCustomer(UpdateView):
    template_name = 'orcamento_marcus/update_customer.html'
    model = Customer
    success_url = reverse_lazy('list_customer')

    def form_valid(self, form):
        messages.success(self.request, _(u'Cliente alterado com sucesso'))
        return super(UpdateCustomer, self).form_valid(form)


class UpdateTypePaint(UpdateView):
    template_name = 'orcamento_marcus/update_type_paint.html'
    model = TypePaint
    success_url = reverse_lazy('list_type_paint')

    def form_valid(self, form):
        messages.success(self.request, _(u'Tipo de pintura atualizado com sucesso'))
        return super(UpdateTypePaint, self).form_valid(form)


class UpdateRoom(UpdateView):
    template_name = 'orcamento_marcus/update_room.html'
    model = Room
    success_url = reverse_lazy('list_room')

    def form_valid(self, form):
        messages.success(self.request, _(u'Comodo atualizado com sucesso'))
        return super(UpdateRoom, self).form_valid(form)


class UpdateWall(UpdateView):
    template_name = 'orcamento_marcus/update_wall.html'
    model = TypeWall
    success_url = reverse_lazy('list_wall')

    def form_valid(self, form):
        messages.success(self.request, _(u'Parede atualizada com sucesso'))
        return super(UpdateWall, self).form_valid(form)


class CreateBudget(CreateView):
    template_name = 'orcamento_marcus/create_budget.html'
    model = Budget
    success_url = reverse_lazy('list_budget')
    form_class = FormBudget

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        rooms = []
        total_value_budget = 0
        for room, id_room in data.iteritems():
            if room != 'csrfmiddlewaretoken' and room != 'customer':
                new_room = Room.objects.get(id=id_room)
                total_value_budget += new_room.total_value_room
                rooms.append(new_room)
        self.object = self.model()
        self.object.customer = Customer.objects.get(id=data['customer'])
        self.object.total_value_budget = total_value_budget
        self.object.save()
        for room in rooms:
            self.object.rooms.add(room)

        return HttpResponseRedirect(reverse('detail_budget', args=(self.object.id,)))

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
            kwargs['form_rooms'] = Room.objects.all()
            kwargs['form_customers'] = Customer.objects.all()
        return super(CreateBudget, self).get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, _(u'Budget criado com sucesso'))
        return super(CreateBudget, self).form_valid(form)


class CreateCustomer(CreateView):
    template_name = 'orcamento_marcus/create_customer.html'
    model = Customer
    success_url = reverse_lazy('list_customer')

    def form_valid(self, form):
        messages.success(self.request, _(u'Cliente cadastrado com sucesso'))
        return super(CreateBudget, self).form_valid(form)


class CreateTypePaint(CreateView):
    template_name = 'orcamento_marcus/create_type_paint.html'
    model = TypePaint
    success_url = reverse_lazy('list_type_paint')
    form_class = FormTypePaint

    def form_valid(self, form):
        messages.success(self.request, _(u'Tipo de pintura cadastrado com sucesso'))
        return super(CreateTypePaint, self).form_valid(form)


class CreateRoom(CreateView):
    template_name = 'orcamento_marcus/create_room.html'
    model = Room
    form_class = FormRoom


    def post(self, request, *args, **kwargs):
        data_posted = request.POST.copy()
        walls = []
        for wall, id_wall in data_posted.iteritems():
            if wall != 'csrfmiddlewaretoken':
                wall = TypeWall.objects.get(pk=id_wall)
                walls.append(wall)
        total_value_room = 0
        for val in walls:
            value_paint = TypePaint.objects.get(id=val.type_paint_id)
            total_value_room += (val.m2 * value_paint.value) - (val.m2_discount * value_paint.value)

        self.object = self.model()
        self.object.total_value_room = total_value_room

        self.object.save()

        for val in walls:
            self.object.walls.add(val)
        return HttpResponseRedirect(reverse('detail_room', args=(self.object.id,)))

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
            kwargs['form_walls'] = TypeWall.objects.all()
        return super(CreateRoom, self).get_context_data(**kwargs)

    def form_valid(self, form):
        messages.success(self.request, _(u'Comodo cadastrado com sucesso'))
        return super(CreateRoom, self).form_valid(form)


class CreateWall(CreateView):
    template_name = 'orcamento_marcus/create_wall.html'
    model = TypeWall
    form_class = FormWall
    success_url = reverse_lazy('list_wall')

    def form_valid(self, form):
        messages.success(self.request, _(u'Parede cadastrada com sucesso'))
        return super(CreateWall, self).form_valid(form)



class DetailRoom(DetailView):
    model = Room
    http_method_names = [u'get', ]
    template_name = 'orcamento_marcus/detail_room.html'


class DetailBudget(DetailView):
    model = Budget
    http_method_names = [u'get', ]
    template_name = 'orcamento_marcus/detail_budget.html'


class ListBudget(ListView):
    template_name = 'orcamento_marcus/list_budget.html'
    model = Budget

    def get_context_object_name(self, object_list):
        for a in object_list:
            qtde_rooms = a.rooms.count()
            setattr(a, 'rooms_count', qtde_rooms)

        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.model_name
        else:
            return None


class ListWall(ListView):
    template_name = 'orcamento_marcus/list_wall.html'
    model = TypeWall

    def get_context_object_name(self, object_list):
        for a in object_list:
            value_paint = TypePaint.objects.get(id=a.type_paint_id)
            setattr(a, 'total', (a.m2 * value_paint.value) - (a.m2_discount * value_paint.value))
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.model_name
        else:
            return None

class ListPaint(ListView):
    template_name = 'orcamento_marcus/list_paint.html'
    model = TypePaint


class ListCustomer(ListView):
    template_name = 'orcamento_marcus/list_customer.html'
    model = Customer


class ListRoom(ListView):
    template_name = 'orcamento_marcus/list_room.html'
    model = Room

    def get_context_object_name(self, object_list):
        for a in object_list:
            qtde_walls = a.walls.count()
            qtde_value_m2 = 0
            qtde_value_m2_discount = 0
            value_room = 0

            for qtde in a.walls.distinct():
                value_paint = TypePaint.objects.get(id=qtde.type_paint_id)
                qtde_value_m2 += qtde.m2
                qtde_value_m2_discount += qtde.m2_discount
                value_room += (qtde.m2 * value_paint.value) - (qtde.m2_discount * value_paint.value)
            setattr(a, 'value_room', value_room)
            setattr(a, 'm2_room', qtde_value_m2)
            setattr(a, 'm2_room_discount', qtde_value_m2_discount)
            setattr(a, 'wall_count', qtde_walls)

        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.model_name
        else:
            return None