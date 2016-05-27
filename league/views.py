from django.views.generic.base import TemplateView


class MainView(TemplateView):
    template_name = 'main.html'
