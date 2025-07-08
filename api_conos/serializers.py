from rest_framework import serializers
from .models import PedidoCono
from api_conos.services.patrones import ConoFactory, ConoBuilder, LoggerSingleton


class PedidoConoSerializer(serializers.ModelSerializer):
    precio_final = serializers.SerializerMethodField()
    ingredientes_finales = serializers.SerializerMethodField()


    class Meta:
        model = PedidoCono
        fields = '__all__'
        

    def get_precio_final(self, obj):
        cono_base = ConoFactory.crear_cono(obj.variante)
        builder = ConoBuilder(cono_base)
        builder.agregar_toppings(obj.toppings)
        LoggerSingleton().log(f"Cálculo precio de {obj.cliente}")
        return builder.obtener_precio()

    def get_ingredientes_finales(self, obj):
        cono_base = ConoFactory.crear_cono(obj.variante)
        builder = ConoBuilder(cono_base)
        builder.agregar_toppings(obj.toppings)
        LoggerSingleton().log(f"Cálculo ingredientes de {obj.cliente}")
        return builder.obtener_ingredientes()
