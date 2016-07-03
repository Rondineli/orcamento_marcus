"""orcamentos_marcus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from orcamentos_marcus.views import (
	DeleteBudget,
	DeleteCustomer,
	DeleteTypePaint,
	DeleteRoom,
	DeleteWall,
	
	UpdateBudget,
	UpdateCustomer,
	UpdateTypePaint,
	UpdateRoom,
	UpdateWall,

	CreateBudget,
	CreateCustomer,
	CreateTypePaint,
	CreateRoom,
	CreateWall,
	
	ListBudget,
	ListWall,
	ListPaint,
	ListCustomer,
	ListRoom,

	DetailRoom,
	DetailBudget
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #Details
    url(r'^detail/room/(?P<pk>\d+)/$', DetailRoom.as_view(), name='detail_room'),
    url(r'^detail/budget/(?P<pk>\d+)/$', DetailBudget.as_view(), name='detail_budget'),
    #Delete
    url(r'^delete/budget/(?P<pk>\d+)/$', DeleteBudget.as_view(), name='delete_budget'),
    url(r'^delete/customer/(?P<pk>\d+)/$', DeleteCustomer.as_view(), name='delete_customer'),
    url(r'^delete/type_paint/(?P<pk>\d+)/$', DeleteTypePaint.as_view(), name='delete_type_paint'),
    url(r'^delete/room/(?P<pk>\d+)/$', DeleteRoom.as_view(), name='delete_room'),
    url(r'^delete/wall/(?P<pk>\d+)/$', DeleteBudget.as_view(), name='delete_wall'),
    #Create
    url(r'^create/budget/$', CreateBudget.as_view(), name='create_budget'),
    url(r'^create/customer/$', CreateCustomer.as_view(), name='create_customer'),
    url(r'^create/type_paint/$', CreateTypePaint.as_view(), name='create_type_paint'),
    url(r'^create/room/$', CreateRoom.as_view(), name='create_room'),
    url(r'^create/wall/$', CreateWall.as_view(), name='create_wall'),
    #Update
    url(r'^update/budget/(?P<pk>\d+)/$', UpdateBudget.as_view(), name='update_budget'),
    url(r'^update/customer/(?P<pk>\d+)/$', UpdateCustomer.as_view(), name='update_customer'),
    url(r'^update/type_paint/(?P<pk>\d+)/$', UpdateTypePaint.as_view(), name='update_type_paint'),
    url(r'^update/room/(?P<pk>\d+)/$', UpdateRoom.as_view(), name='update_room'),
    url(r'^update/wall/(?P<pk>\d+)/$', UpdateWall.as_view(), name='update_wall'),
    #List
    url(r'^list/budget/$', ListBudget.as_view(), name='list_budget'),
    url(r'^list/wall/$', ListWall.as_view(), name='list_wall'),
    url(r'^list/type_paint/$', ListPaint.as_view(), name='list_type_paint'),
    url(r'^list/customer/$', ListCustomer.as_view(), name='list_customer'),
    url(r'^list/room/$', ListRoom.as_view(), name='list_room'),
]
