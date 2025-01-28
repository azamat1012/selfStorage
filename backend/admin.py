from django.contrib import admin
from backend.models import StorageBox, StorageUser, Order, Delivery, Promotion

admin.site.register(StorageBox)
admin.site.register(StorageUser)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Promotion)
