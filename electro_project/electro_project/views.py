from django.views.generic import TemplateView

from electro_social.models import UserInfo


class IndexView(TemplateView):
    template_name = 'index.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

