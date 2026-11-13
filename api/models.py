from django.db import models
from django.contrib.auth.models import User

class NotesLoan(models.Model):
    full_name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    phone = models.CharField(max_length=13)
    is_paid = models.BooleanField(default=False)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
        
    def __str__(self):
        return self.user_id
    
    