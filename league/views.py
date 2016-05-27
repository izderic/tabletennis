from django.views.generic.base import TemplateView

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RankingSerializer
from .models import League


class MainView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        return super(MainView, self).get_context_data(**kwargs)


class RankingList(APIView):
    def get(self, request, format=None):
        league_id = self.request.query_params.get('league')
        league = League.objects.get(pk=league_id)
        serializer = RankingSerializer(league.get_rankings(), many=True)
        return Response(serializer.data)
