from django.db import models
import uuid

# Create your models here.

# This is only one model which saves in db to get back all ids from multiple banks
class RequisitonId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requisitionId= models.CharField(max_length=255, null=True, blank=True)
    bankName = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.bankName)