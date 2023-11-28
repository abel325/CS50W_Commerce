from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing_page/<int:listing_id>", views.listing_page, name='listing_page'),
    path('add_to_watchlist/<int:listing_id>', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_from_watchlist/<int:listing_id>', views.remove_from_watchlist, name='remove_from_watchlist'),
    path('bid/<int:listing_id>', views.bid, name='bid'),
    path('close_listing/<int:listing_id>', views.close_listing, name='close_listing'),
    path('delete_listing/<int:listing_id>', views.delete_listing, name='delete_listing'),
    path('my_listings', views.my_listings, name='my_listings'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('won_listings', views.won_listings, name='won_listings'),
]
