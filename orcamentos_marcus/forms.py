# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from orcamentos_marcus.models import (
    TypePaint,
    TypeWall,
    Room,
    Customer,
    Budget
)


class FormTypePaint(forms.ModelForm):
	class Meta:
		model = TypePaint
		fields = '__all__'
		widgets = {
			'type_description': forms.Select(
				attrs={
					'class': 'browser-default',
					'type': 'text'
				}
			)
		}


class FormBudget(forms.ModelForm):
	class Meta:
		model = Budget
		fields = '__all__'


class FormRoom(forms.ModelForm):
	class Meta:
		model = Room
		fields = '__all__'


class FormWall(forms.ModelForm):
	class Meta:
		model = TypeWall
		fields = [ 'type_paint', 'm2', 'm2_discount' ]
		widgets = {
			'type_paint': forms.Select(
				attrs={
					'class': 'browser-default',
					'type': 'text'
				}
			)

		}