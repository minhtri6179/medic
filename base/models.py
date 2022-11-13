from django.db import models
from django.utils import timezone

# Create your models here.
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class SoftDeleteAbstractModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)
    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
    def restore(self):
        self.deleted_at = None
        self.save()
    
    class Meta:
        abstract = True