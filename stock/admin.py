from django.contrib import admin, messages
from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError

from .models import Producto, Lote, MovimientoStock

# Branding (opcional)
admin.site.site_header = "PharmaMaster – Administración"
admin.site.site_title = "PharmaMaster Admin"
admin.site.index_title = "Panel de Stock y Trazabilidad"


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "gtin", "nombre", "laboratorio", "estado", "actualizado_en")
    search_fields = ("gtin", "nombre", "laboratorio")
    list_filter = ("estado",)
    ordering = ("-id",)
    list_per_page = 25


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ("id", "producto", "numero_lote", "fecha_venc", "stock")
    list_filter = ("fecha_venc", "producto")
    search_fields = ("numero_lote", "producto__nombre", "producto__gtin")
    ordering = ("fecha_venc", "producto__nombre")
    list_per_page = 25


@admin.register(MovimientoStock)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tipo",
        "cantidad",
        "lote",
        "stock_antes",
        "stock_despues",
        "usuario",
        "aplicado_en",
        "documento_ref",
    )
    list_filter = ("tipo", "aplicado_en", "usuario")
    search_fields = (
        "motivo",
        "documento_ref",
        "lote__numero_lote",
        "lote__producto__nombre",
        "lote__producto__gtin",
    )
    date_hierarchy = "aplicado_en"
    ordering = ("-aplicado_en", "-id")
    readonly_fields = ("creado_en", "aplicado_en", "stock_antes", "stock_despues", "usuario")
    list_per_page = 25
    actions = ["aplicar_movimientos"]

    def has_change_permission(self, request, obj=None):
        """
        Evitar editar un movimiento ya aplicado (auditoría).
        """
        if obj and obj.aplicado_en:
            return False
        return super().has_change_permission(request, obj)

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        """
        Al guardar desde Admin: adjunta usuario y aplica si aún no fue aplicado.
        """
        # Si ya está aplicado, no permitir re-aplicar
        if obj.aplicado_en:
            super().save_model(request, obj, form, change)
            return

        # Seteamos usuario (auditoría)
        if not obj.usuario:
            obj.usuario = request.user

        # Guardado preliminar para obtener PK (si es alta)
        if not change or obj.pk is None:
            super().save_model(request, obj, form, change)

        # Aplicar impacto en stock + sellar auditoría
        try:
            obj.aplicar()
            messages.success(request, f"Movimiento {obj.id} aplicado. Stock {obj.stock_antes} → {obj.stock_despues}.")
        except DjangoValidationError as e:
            # Revertir si hubo error de negocio (stock negativo, lote vencido, etc.)
            raise

    @admin.action(description="Aplicar movimientos seleccionados (si no están aplicados)")
    def aplicar_movimientos(self, request, queryset):
        pendientes = queryset.filter(aplicado_en__isnull=True).select_related("lote")
        ok = 0
        err = 0
        for mov in pendientes.order_by("id"):
            try:
                if not mov.usuario:
                    mov.usuario = request.user
                mov.aplicar()
                ok += 1
            except DjangoValidationError as e:
                err += 1
        if ok:
            self.message_user(request, f"{ok} movimientos aplicados correctamente.", level=messages.SUCCESS)
        if err:
            self.message_user(request, f"{err} movimientos con error (ver detalles en cada registro).", level=messages.WARNING)