from django.contrib import admin
from product.models import product, transaction,comments
# Register your models here.

admin.site.register(product)
admin.site.register(transaction)
admin.site.register(comments)

