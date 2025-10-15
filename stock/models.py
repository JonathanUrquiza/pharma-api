from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.db.models import Q


# -------------------------
# Helpers / Validadores
# -------------------------
def validar_ean13(value: str):
    s = "".join(ch for ch in (value or "") if ch.isdigit())
    if len(s) != 13:
        raise ValidationError("GTIN/EAN-13 debe tener 13 dígitos")
    digits = list(map(int, s))
    check = digits.pop()
    calc = (10 - (sum(d if i % 2 == 0 else d * 3 for i, d in enumerate(digits)) % 10)) % 10
    if calc != check:
        raise ValidationError("GTIN/EAN-13 con dígito verificador inválido")


# -------------------------
# Producto
# -------------------------
class Producto(models.Model):
    gtin = models.CharField(max_length=14, unique=True, validators=[validar_ean13])
    nombre = models.CharField(max_length=200)
    laboratorio = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=10, default='activo')  # activo/inactivo
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.gtin})"


# -------------------------
# Lote
# -------------------------
class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    numero_lote = models.CharField(max_length=80)
    fecha_venc = models.DateField()
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ('producto', 'numero_lote')
        constraints = [
            # stock nunca negativo (también a nivel BD)
            models.CheckConstraint(check=Q(stock__gte=0), name='ck_lote_stock_no_negativo'),
        ]
        indexes = [
            models.Index(fields=['producto', 'numero_lote']),
            models.Index(fields=['fecha_venc']),
        ]

    def clean(self):
        if self.stock < 0:
            raise ValidationError("El stock inicial no puede ser negativo")

    def __str__(self):
        return f"Lote {self.numero_lote} - {self.producto.nombre}"


# -------------------------
# MovimientoStock (auditoría)
# -------------------------
class MovimientoStock(models.Model):
    TIPOS = (('INGRESO','INGRESO'), ('EGRESO','EGRESO'), ('AJUSTE','AJUSTE'))

    lote = models.ForeignKey('Lote', on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=255, blank=True)
    documento_ref = models.CharField(max_length=100, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    # --- AUDITORÍA ---
    aplicado_en = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='movimientos_stock'
    )
    stock_antes = models.IntegerField(null=True, blank=True)
    stock_despues = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        constraints = [
            # cantidad no puede ser 0
            models.CheckConstraint(check=~Q(cantidad=0), name='ck_mov_cantidad_no_cero'),
            # signo por tipo: INGRESO/EGRESO > 0, AJUSTE puede ser +/- (pero aplicar() ya evita < 0 final)
            models.CheckConstraint(
                check=Q(tipo='AJUSTE') | (Q(tipo__in=['INGRESO','EGRESO']) & Q(cantidad__gt=0)),
                name='ck_mov_signo_por_tipo'
            ),
        ]
        indexes = [
            models.Index(fields=['lote', 'creado_en']),
            models.Index(fields=['aplicado_en']),
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"{self.tipo} {self.cantidad} en {self.lote}"

    def clean(self):
        # reglas de negocio básicas (coherentes con las constraints)
        if self.cantidad == 0:
            raise ValidationError({"cantidad": "La cantidad no puede ser 0."})
        if self.tipo in {"INGRESO", "EGRESO"} and self.cantidad < 0:
            raise ValidationError({"cantidad": "Use cantidad positiva en INGRESO/EGRESO. En AJUSTE se permite negativa."})
        if self.tipo not in {"INGRESO", "EGRESO", "AJUSTE"}:
            raise ValidationError({"tipo": "Tipo inválido."})

    @transaction.atomic
    def aplicar(self):
        """
        Aplica el movimiento al stock del lote con lock de fila y completa auditoría.
        - Prohíbe stock negativo.
        - Sella aplicado_en, usuario, stock_antes/stock_despues.
        """
        l = Lote.objects.select_for_update().get(pk=self.lote_id)
        self.stock_antes = l.stock

        if self.tipo == 'INGRESO':
            nuevo = l.stock + abs(self.cantidad)

        elif self.tipo == 'EGRESO':
            # bloqueo de vencidos (comenta si no lo necesitás)
            if l.fecha_venc and l.fecha_venc < timezone.now().date():
                raise ValidationError({"lote": "Lote vencido: no se permite egreso."})
            nuevo = l.stock - abs(self.cantidad)
            if nuevo < 0:
                raise ValidationError({"cantidad": "Stock insuficiente: el egreso dejaría stock negativo."})

        else:  # AJUSTE
            nuevo = l.stock + self.cantidad
            if nuevo < 0:
                raise ValidationError({"cantidad": "Ajuste inválido: stock no puede quedar negativo."})

        # persistir
        l.stock = nuevo
        l.save(update_fields=["stock"])

        # auditoría
        self.stock_despues = nuevo
        self.aplicado_en = timezone.now()

        if not self.pk:
            super().save()
        else:
            super().save(update_fields=["stock_antes", "stock_despues", "aplicado_en", "usuario"])

        return self