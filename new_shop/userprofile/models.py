from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import product

class cart(models.Model):
    user = models.OneToOneField(User)
    kart=models.CharField(max_length=70)

    def __unicode__(self):
        
        return (str(self.user.username))
    
    
User.cart = property(lambda u: cart.objects.get_or_create(user=u)[0])

class user_hist(models.Model):
    user = models.ForeignKey(User)
    u_hist=models.ForeignKey(product)

    def __unicode__(self):
        
        return (str(self.user.username)+' '+str(self.product.name))
 
