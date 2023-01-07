from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="add_watchlist"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="remove_watchlist"),
    path("diactivate/<int:listing_id>", views.diactivate, name="diactivate"),
    path("addComment/<int:listing_id>", views.addComment, name="add_comment")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
