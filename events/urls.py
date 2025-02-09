from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('event/', views.event, name='event'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create_staff/', views.create_staff, name='create_staff'),
    path('view_purchases/', views.view_purchases, name='view_purchases'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('create_merch/', views.create_merch, name='create_merch'),
    path('update_merch/<int:merch_id>/', views.update_merch, name='update_merch'),
    path('delete_merch/<int:item_id>/', views.delete_merch, name='delete_merch'),
    path('create_event/', views.create_event, name='create_event'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:item_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('merch/', views.merch, name='merch'),
    path('purchase_merch/<int:item_id>/', views.purchase_merch, name='purchase_merch'),
    path('participate_event/<int:event_id>/', views.participate_event, name='participate_event'),
    path('purchase_event_ticket/<int:event_id>/', views.purchase_event_ticket, name='purchase_event_ticket'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('dashboard_redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('track_staff/', views.track_staff, name='track_staff'), 
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('delete_merch/<int:item_id>/', views.delete_merch, name='delete_merch'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
