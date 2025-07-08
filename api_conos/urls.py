from rest_framework.routers import DefaultRouter
from .views import PedidoConoViewSet

router = DefaultRouter()
router.register(r'pedidos_conos', PedidoConoViewSet)

urlpatterns = router.urls
