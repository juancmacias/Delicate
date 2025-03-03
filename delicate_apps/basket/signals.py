from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BasketTemp

@receiver(post_save, sender=BasketTemp)
def create_invoice_on_basket_save(sender, instance, created, **kwargs):
    if created:
        from delicate_apps.invoices.models import Invoice, InvoiceItem
        try:
            # Create a new invoice
            invoice = Invoice.objects.create(
                date=timezone.now().date(),
                payment_form='Efectivo',
                neto=instance.get_total_with_iva(),
                fk_user=instance.user_id,
                fk_company=instance.user_id.company,  # Usar company en lugar de fk_company
                fk_type=instance.product_id.fk_type
            )

            # Create invoice details
            InvoiceItem.objects.create(
                invoice=invoice,
                product=instance.product_id,
                quantity=instance.cantidad,
                price=instance.precio
            )

            # Update stock of product
            product = instance.product_id
            product.stock -= instance.cantidad
            product.save()

        except Exception as e:
            print(f"Error creando factura: {str(e)}")