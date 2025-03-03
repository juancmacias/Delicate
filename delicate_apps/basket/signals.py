from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BasketTemp
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=BasketTemp)
def create_invoice_on_basket_save(sender, instance, created, **kwargs):
    if created:
        from delicate_apps.invoices.models import Invoice, InvoiceItem
        try:
            logger.info(f"Creando factura para item de cesta {instance.id}")
            
            # Crear factura
            total = float(instance.get_total_with_iva())
            logger.info(f"Total calculado: {total}")
            
            invoice = Invoice.objects.create(
                date=timezone.now().date(),
                payment_form='Efectivo',
                neto=total,
                fk_user=instance.user_id,
                fk_company=instance.user_id.company,
                fk_type=instance.product_id.fk_type
            )
            logger.info(f"Factura creada con ID: {invoice.id}")

            # Crear detalle de factura
            invoice_item = InvoiceItem.objects.create(
                invoice=invoice,
                product=instance.product_id,
                quantity=instance.cantidad,
                price=float(instance.precio)
            )
            logger.info(f"Detalle de factura creado con ID: {invoice_item.id}")

            # Actualizar stock
            product = instance.product_id
            product.stock -= instance.cantidad
            product.save()
            logger.info(f"Stock actualizado para producto {product.id}")

        except Exception as e:
            logger.error(f"Error creando factura: {str(e)}", exc_info=True)
            print(f"Error creando factura: {str(e)}")