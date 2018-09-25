# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic.base import TemplateView
from sites.models import Sites, SitesValues
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

# Create your views here.


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['sites'] = Sites.objects.all().order_by('-created_on')
        return context


class DetailView(TemplateView):

    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        try:
            name = Sites.objects.get(id=self.kwargs["pk"]).name
            vobj = SitesValues.objects.filter(site_id=self.kwargs["pk"])
            resp_dict = {"values": vobj, "name": name}
            context['detail'] = resp_dict
        except ObjectDoesNotExist as e:
            context['detail'] = {}
        return context


class SumView(TemplateView):

    template_name = "summary.html"

    def get_context_data(self, **kwargs):
        context = super(SumView, self).get_context_data(**kwargs)
        site_dict = {}
        for i in Sites.objects.all():
            site_dict[i.id] = i.name
        vobj = SitesValues.objects.all().values('site_id').order_by('site_id').annotate(a_total=Sum('a_value')).annotate(b_total=Sum('b_value'))
        for v in vobj:
            v["name"] = site_dict.get(v["site_id"])
        context['summary'] = vobj
        return context


class AverageView(TemplateView):

    template_name = "summary.html"

    def get_context_data(self, **kwargs):
        context = super(AverageView, self).get_context_data(**kwargs)
        try:
            site_dict = {}

            for i in Sites.objects.all():
                site_dict[i.id] = {"name": i.name, "count": 0, "a_total": 0, "b_total": 0}

            for val in SitesValues.objects.all():
                temp = val.site_id
                if site_dict.get(temp):
                    vdict = site_dict.get(temp)
                    vdict["a_total"] += val.a_value
                    vdict["b_total"] += val.b_value
                    vdict["count"] += 1
                    site_dict[temp] = vdict
            master_list = []
            for k, v in site_dict.iteritems():
                a_avg = v["a_total"] / v["count"]
                b_avg = v["b_total"] / v["count"]
                v["a_total"] = float("{0:.2f}".format(a_avg))
                v["b_total"] = float("{0:.2f}".format(b_avg))
                master_list.append(v)
            context['summary'] = master_list
        except ObjectDoesNotExist as e:
            context['summary'] = []
        return context