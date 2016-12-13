from django.db import connection
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import classonlymethod
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import BaseUserManager, User
from django.http import HttpResponse
from django.contrib.admin import ModelAdmin
import logging
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.views.generic.base import TemplateView
from utils import get_permission_codename
from mixins  import item, dashboardItemsMixin
from options import ModelAllViews
from django.contrib.auth.models import User, Group
from . import models
from . import utils
from django.conf.urls import url
import django.db.models.aggregates as agg
from django.db.models import Case, Value, When, F
from django.db.models.functions import Coalesce


class helloLoginView(TemplateView):
    """ display the login page """
    template_name = 'supplychain/helloLogin.html'
    @property
    def guest(self):
        guest = settings.GUEST_LOGIN
        return authenticate(username=guest)

class LoginView(helloLoginView):
    """ display the login page on get, accept login on post """
    def post(self, request):
        user_name = request.POST['user_name']
        user_pass = request.POST['user_pass']
        logging.info("Login Attempt by " + user_name )
        user = authenticate(username=user_name, password=user_pass)
        if user:
            login(request, user)
            return HttpResponse('successful')
        else:
            return HttpResponse('invalid login/password')

class dashboard(dashboardItemsMixin, LoginRequiredMixin, TemplateView):
    """ the dashboard page """
    template_name = 'supplychain/dashboard.html'

class StatusView(dashboardItemsMixin, TemplateView):
    template_name = 'supplychain/status.html'

    def volume(self):
        return utils.addDollarSign(models.Order.objects.aggregate(agg.Sum('price'))['price__sum'])

    def _all_company_payable(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            select c.name, COALESCE(
            sum(Case
            		when ordertype='SELLOUT'
            		then price
            		else price * -1
            	end), 0)
            From supplychain.supplychain_company as c LEFT JOIN supplychain.supplychain_order as o
            on c.id = o.company_id
            group by c.name
            order by c.name;
                    """)
            return cursor.fetchall()

    def _company_transaction(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            select co.name, sum(OT.sum)
	           From
               (supplychain.supplychain_company as co
		             Inner Join
		                   (select * from
                        (SELECT tr.fr_account_id as id, COALESCE(sum(tr.amount), 0) as sum
					From supplychain.supplychain_transaction as tr
                    group by tr.fr_account_id) as T1 Union
	                   (SELECT tr.to_account_id as id, COALESCE(sum(-tr.amount), 0) as sum
					From supplychain.supplychain_transaction as tr
                    group by tr.to_account_id) )as OT
		                  On co.id = OT.id)
                          group by co.name
                          order by co.name;
                    """
                    )
            return cursor.fetchall()

    def _capital_total(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            select T1.name, transaction, payable, (payable - transaction) as balance from(
select co.name, sum(OT.sum) as transaction
	From
    (supplychain.supplychain_company as co
		Inner Join
		(select * from
	(SELECT tr.fr_account_id as id, COALESCE(sum(tr.amount), 0) as sum
					From supplychain.supplychain_transaction as tr
                    group by tr.fr_account_id) as T1 Union
	(SELECT tr.to_account_id as id, COALESCE(sum(-tr.amount), 0) as sum
					From supplychain.supplychain_transaction as tr
                    group by tr.to_account_id) )as OT
		On co.id = OT.id)
group by co.name
order by co.name
)as T2
Inner Join
(select c.name, COALESCE(
            sum(Case
            		when ordertype='SELLOUT'
            		then price
            		else price * -1
            	end), 0) as payable
            From supplychain.supplychain_company as c LEFT JOIN supplychain.supplychain_order as o
            on c.id = o.company_id
            group by c.name
            order by c.name) as T1
on T1.name = T2.name
                    """
                    )
            return cursor.fetchall()

    def _inv_total(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            select inventory_id, sum(item_size) as Size_used, inv_size as Total_size, (inv_size - sum(item_size)) as Available_size
from(
SELECT T1.catalog_id, T1.inventory_id, T2.id, T2.size as item_size, T3.size as inv_size
FROM
supplychain.supplychain_item as T1,
supplychain.supplychain_catalog as T2,
supplychain.supplychain_inventory as T3
WHERE T1.catalog_id = T2.id and T1.inventory_id = T3.id
) as tt
group by inventory_id
                    """
                    )
            return cursor.fetchall()

    def _order_total(self):
        with connection.cursor() as cursor:
            cursor.execute("""
            Select Tr.order_id, price, ordertype,state,itemID_list from
(SELECT order_id, price, ordertype,ItemID_list from
	(supplychain.supplychain_order as Ord
		Inner Join
        (Select * from
			(SELECT group_concat(id) as ItemID_list, order_id
			FROM supplychain.supplychain_item
			WHERE order_id <> 0
			group by order_id)
            as ttt
		) as Ord_Item
on Ord_Item.order_id = Ord.id)) as order_item
Inner Join
(SELECT order_id, amount, state from supplychain.supplychain_transaction) as Tr
on order_item.order_id = Tr.order_id
Where state <> "COMPELTED"
                    """
                    )
            return cursor.fetchall()

    def inv_total(self):
        bs = self._inv_total()
        return [(b[0], b[1], b[2], b[3]) for b in bs]


    def capital_total(self):
        bs = self._capital_total()
        return [(b[0], utils.addDollarSign(b[1]), utils.addDollarSign(b[2]), utils.addDollarSign(b[3])) for b in bs]

    def order_total(self):
        bs = self._order_total()
        return [(b[0], b[1], b[2], b[3], b[4]) for b in bs]


    def all_company_payable(self):
        bs = self._all_company_payable()
        return [(b[0], utils.addDollarSign(b[1])) for b in bs]

    def company_transaction(self):
        bs = self._company_transaction()
        return [(b[0], utils.addDollarSign(b[1])) for b in bs]

    def all_company_balance(self):
        bs = self._all_company_payable()
        ts = self._company_transaction()
        return [(b[0], utils.addDollarSign(b[1] - t[1])) for b, t in zip(bs, ts)]

    def all_inventory_count(self):
        return models.Item.objects.values_list('inventory__name').annotate(
                agg.Count('id'))


class StatusUrls(object):
    urls = urlpatterns = [
            url(r'^$', StatusView.as_view(), name='status'),
        ]

class dashboardItems(object):
    """ generate urls and models """
    items = dashboardItemsMixin.items
    from django.conf.urls import url, include
    ItemModels =  [StatusUrls] + [ModelAllViews(model) for model in [User, Group,\
                        models.Company, models.Inventory, models.Catalog, models.Account,\
                        models.Order, models.Transaction, models.Order_Item \
                        , models.Item, ]] \
                + [models.BetUrls, models.CountUrls ]
    urls = [url(item.url[1:], include(ItemModels[i].urls)) for i, item in enumerate(items)]
