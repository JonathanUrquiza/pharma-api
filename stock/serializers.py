from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from .models import Producto, Lote, MovimientoStock


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = ("id", "numero_lote", "fecha_venc", "stock", "producto")


class ProductoSerializer(serializers.ModelSerializer):
    lotes = LoteSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = ("id", "gtin", "nombre", "laboratorio", "estado", "lotes")


class MovimientoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoStock
        fields = (
            "id",
            "lote",
            "tipo",
            "cantidad",
            "motivo",
            "documento_ref",
            "creado_en",
            "aplicado_en",
            "usuario",
            "stock_antes",
            "stock_despues",
        )
        read_only_fields = ("creado_en", "aplicado_en", "usuario", "stock_antes", "stock_despues")

    def create(self, validated_data):
        """
        Crea el movimiento, adjunta usuario (si hay), valida reglas de negocio
        y aplica el impacto en stock en forma atómica.
        """
        mov = MovimientoStock(**validated_data)

        # Adjuntar usuario autenticado (auditoría)
        req = self.context.get("request")
        if req and getattr(req, "user", None) and req.user.is_authenticated:
            mov.usuario = req.user

        # Validación de nivel modelo (llama a clean())
        mov.full_clean()

        # Guardar y aplicar (manejo de errores a DRF)
        try:
            mov.save()
            mov.aplicar()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict or e.messages)

        return mov