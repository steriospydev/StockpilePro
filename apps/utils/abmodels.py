from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class AbstractModel(models.Model):
    created_at = models.DateTimeField('Δημιουργηθηκε', auto_now_add=True)
    updated_at = models.DateTimeField('Ανανεωθηκε', auto_now=True)
    is_active = models.BooleanField("Active", default=True)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        abstract = True
