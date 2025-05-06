from django.db import models

# Create your models here..
class Contact(models.Model):
    
     name = models.CharField(max_length=122)
     username = models.CharField(max_length=122)
     email = models.EmailField()
     contact = models.CharField(max_length=12)
     address = models.CharField(max_length=225)
     comment = models.TextField()
     date = models.DateField()
     
     
     
     def __str__(self):
        return self.name