from rest_framework import viewsets
from .models import PedidoCono
from .serializers import PedidoConoSerializer

class PedidoConoViewSet(viewsets.ModelViewSet):
    queryset = PedidoCono.objects.all()
    serializer_class = PedidoConoSerializer
