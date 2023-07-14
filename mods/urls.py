from django.urls import path,re_path
from django.views.i18n import JavaScriptCatalog
from . import views

urlpatterns = [
    path("", views.ViewHome),
    #path("<str:game_slug>/", views.ViewGame),
    path("<str:game_slug>/mods/", views.ModList.as_view(), name='view_mods'),
    path("<str:game_slug>/mod/<int:id_slug>/", views.ViewMod),
    path("<str:game_slug>/mod/<str:author_name>/<str:id_slug>/", views.ViewMod, name='view_mod'),
    path("<str:game_slug>/submit/", views.ViewSubmit, name = 'submit_mod'),
    path("<str:game_slug>/submit/<int:id>/", views.ViewSubmit, name = 'submit_mod'),
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='jsi18n'),
    re_path(r'^genres/$', views.show_genres),
]