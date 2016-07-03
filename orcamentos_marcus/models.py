# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import RegexValidator


class DatedModel(models.Model):
    creation_time = models.DateTimeField(
        _(u'data de criação'),
        auto_now_add=True
    )
    modification_time = models.DateTimeField(
        _(u'data de atualização'),
        auto_now=True
    )

    class Meta:
        abstract = True


class TypePaint(DatedModel):
    TYPES_PAINT = (
        (u'texture', _(u'textura')),
        (u'default', _(u'normal'))
    )

    type_description = models.CharField(
        max_length=10,
        choices=TYPES_PAINT,
        verbose_name = _(u'Descricao do tipo de pintura')
    )
    value = models.DecimalField(
        _(u'Valor por m2'),
        decimal_places=2,
        max_digits=200
    )

    def __unicode__(self):
        if self.type_description == 'texture':
            self.type_description_unicode = u'textura'
        else:
            self.type_description_unicode = u'normal'

        return u'R$ {} por m2 de pintura tipo: {}'.format(self.value, self.type_description_unicode)


class TypeWall(DatedModel):
    type_paint = models.ForeignKey(
        'TypePaint',
        verbose_name=_(u'Tipo de pintura'),
        on_delete=models.CASCADE
    )
    m2 = models.DecimalField(
        _(u'tamanho em (M2)'),
        decimal_places=2,
        max_digits=200
    )
    m2_discount = models.DecimalField(
        _(u'Desconto em (M2)'),
        decimal_places=2,
        max_digits=200
    )

    def __unicode__(self):
        return 'criado: {} | m2: {} | m2 desconto: {}'.format(
            self.creation_time.strftime("%d-%m-%Y"),
            self.m2,
            self.m2_discount
        )


class Room(DatedModel):
    walls = models.ManyToManyField(
        'TypeWall',
        verbose_name=_(u'paredes'),
        related_name=_(u'paredes')
    )
    total_value_room = models.DecimalField(
        _(u'Total do comodo'),
        decimal_places=2,
        max_digits=200
    )


class Customer(DatedModel):
    PHONE_REGEX = RegexValidator(
            regex=settings.PHONE_REGEX,
            message=_(u'Telefone deve conter o formato: +5511999999999')
        )
    name = models.CharField(
        max_length=255,
        verbose_name=_(u'Nome do cliente')
    )
    email = models.EmailField(
        _(u'Email')
    )
    phone = models.CharField(
        validators=[PHONE_REGEX],
        blank=False,
        max_length=15
    )

    def __unicode__(Self):
        return 'Novo cliente: {}'.format(self.name)


class Budget(DatedModel):
    rooms = models.ManyToManyField(
        'Room',
        verbose_name=_(u'Comodo')
    )
    total_value_budget = models.DecimalField(
        _(u'Valor total do Orcamento (R$)'),
        decimal_places=2,
        max_digits=200
    )
    customer = models.ForeignKey(
        'Customer'
    )
