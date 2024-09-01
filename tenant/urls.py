from django.urls import path
from . import views

app_name = 'tenant'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('matches/', views.matches, name='matches'),
    path('housing/', views.housing, name='housing'),
    path('house/<int:house_id>/', views.view_house, name='view_house'),
    path('config/', views.stripe_config, name="config"),
    path('create-checkout-session/', views.create_checkout_session, name="create-checkout-session"),
    path('shortlist/<int:house_id>/', views.shortlist_house, name='shortlist_house'),
    path('remove-shortlisted-house/<int:house_id>/', views.remove_shortlisted_house, name='remove_shortlisted_house'),

]