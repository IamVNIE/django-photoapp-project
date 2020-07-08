from django.db import models
from django.contrib.auth.models import User
#from private_storage.fields import PrivateFileField
# Create your models here.
class MYPhotos(models.Model):
    id = models.AutoField(primary_key=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/',  )
    is_public = models.BooleanField(default=False) 
    
    #image = PrivateFileField(upload_to='images/')
    def __str__(self):
        return str(self.id)