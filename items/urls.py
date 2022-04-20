from django.conf.urls.static import static
from django.urls import path

from Ecommerce import settings
from .views import *

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path("chi-tiet-san-pham/<slug>/", ItemDetailView, name="details"),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('gio-hang/', CartView.as_view(), name='cart'),
    path('tim-kiem/', item_search_view, name='search'),
    path('danh-muc/<pk>', filter_by_category, name='filter-by-cate'),
    path('remove-from-cart/<slug>/<size>', remove_from_cart, name='remove-from-cart'),
    path('chi-tiet-don-hang/<pk>', OrderDetailView.as_view(), name='order-details'),
    path('don-hang/', OrderListView.as_view(), name='orders'),
    path('don-hang/dang-xu-ly/', OrderFilter, name='order-filter'),
    path('don-hang/<state>', OrderFilter, name='order-filter'),
    path('order-process-done/<pk>', OrderProcessDone, name='order-process-done'),
    path('cancel-order/<pk>', cancel_order, name='cancel-order'),
    path('remove-single-from-cart/<slug>/<size>/', remove_single_item_from_cart, name='remove-single-from-cart'),
    path('increase-quantity/<slug>/<size>/', increase_quantity, name='increase-quantity'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
