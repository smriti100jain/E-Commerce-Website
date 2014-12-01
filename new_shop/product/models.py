from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class product(models.Model):
    name=models.CharField(max_length=200)
    quantity=models.IntegerField(default=1)
    category=models.CharField(max_length=200)
    description=models.TextField()
    related_prod=models.CharField(max_length=200)
    price=models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

class transaction(models.Model):
    address=models.TextField()
    address_complete=models.TextField()
    delivered=models.BooleanField(default=False)
    user=models.ForeignKey(User)
    product=models.ForeignKey(product)
    quantity=models.IntegerField()
    date=models.DateTimeField('Date Ordered')
    date_complete=models.DateTimeField('Date Delivered')
    

    def __unicode__(self):
        if self.delivered:
            temp='complete'
        else:
            temp='incomplete'
        
        return (str(self.user.username)+' '+str(self.product.name)+' ' + ' '+str(temp))

class comments(models.Model):
    user=models.ForeignKey(User)
    comment=models.TextField()
    product=models.ForeignKey(product)

    def __unicode__(self):
        
        return (str(self.user.username)+' '+str(self.product.name))
