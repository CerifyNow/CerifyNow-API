from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Certificate
from .utils import generate_qr
from .blockchain import save_hash_to_blockchain

@receiver(post_save, sender=Certificate)
def certificate_post_save(sender, instance, created, **kwargs):
    if created:
        tx_hash = save_hash_to_blockchain(instance.hash)
        qr_file = generate_qr(instance.hash)
        instance.qr_code.save(f"{instance.pk}_qr.png", qr_file, save=False)
        instance.save()