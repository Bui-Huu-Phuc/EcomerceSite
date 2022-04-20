from django.contrib import admin
from .models import Item, Category, OrderItem, Order, ItemImage


# Register your models here.

class ItemImageAdmin(admin.StackedInline):
    model = ItemImage


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ["categories"]
    inlines = [ItemImageAdmin]

    class Meta:
        model = Item


@admin.register(ItemImage)
class PostImageAdmin(admin.ModelAdmin):
    pass





class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["ItemName", "quantity", "OrderID"]
    search_fields = ['order']
    list_filter = ["item"]

    def ItemName(self, obj, *args, **kwargs):
        return obj.item.name

    def OrderID(self, obj, *args, **kwargs):
        order_id = Order.objects.get(items=obj.pk)
        return order_id.pk

    class Meta:
        model = OrderItem


admin.site.register(Category)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order)
