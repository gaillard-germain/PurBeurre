from django.db import models

class Favorite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
