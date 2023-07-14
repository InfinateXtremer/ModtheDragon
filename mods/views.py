from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import Q

import random

from .models import *
from .forms import *

# Create your views here.

class ModList(ListView):
    model = Mod
    paginate_by = 20

    def get_queryset(self):
        query = Q()

        game = Game.objects.get(slug=self.kwargs.get('game_slug', None))
        query &= Q(game = game)
        
        get = self.request.GET
        
        if 'query' in get:
            for word in get['query'].split():
               query &= Q(title__icontains = word)

        return self.model.objects.filter(query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        game = Game.objects.get(slug = self.kwargs.get('game_slug', None))
        images = list(GameBackground.objects.filter(game = game))

        context['games'] = Game.objects.all()
        context['game'] = game
        context['game_background'] = None if len(images) == 0 else random.choice(images)

        return context

def ViewHome(request):
    reignited_thumbs = list(GameBackground.objects.filter(game__slug = "spyro-reignited-trilogy"))
    about_time_thumbs = list(GameBackground.objects.filter(game__slug = "crash-4-its-about-time"))
    psx_thumbs = list(GameBackground.objects.filter(game__slug = "spyro-riptos-rage-psx"))

    games = Game.objects.all()
    return render(request, "home.html", {
        "games": games,
        "spyro_bg": None if len(reignited_thumbs) == 0 else random.choice(reignited_thumbs),
        "crash_bg": None if len(about_time_thumbs) == 0 else random.choice(about_time_thumbs),
        "psx_bg": None if len(psx_thumbs) == 0 else random.choice(psx_thumbs),
    })

def ViewMod(request, game_slug, id_slug, author_name):
    mod = None
    games = Game.objects.all()
    #try:
    if type(id_slug) == int:
        mod = Mod.objects.get(game__slug = game_slug, id = id_slug)
    else:
        mod = Mod.objects.get(game__slug = game_slug, slug = id_slug, author__user__username = author_name)
    #except ObjectDoesNotExist:
        #return HttpResponseNotFound()

    return render(request, "mod.html", {"mod": mod, "game": mod.game, "games": games})

@login_required
def ViewSubmit(request, game_slug, id=None):
    game = None
    try:
        is_staff = request.user.is_staff or request.user.is_superuser
        mod = None
        if id:
            try:
                mod = Mod.objects.get(id = id)
                if mod.author == request.user.author or is_staff:
                    game = mod.game
                else:
                    return HttpResponseNotAllowed()
            except ObjectDoesNotExist:
                return HttpResponseNotFound()
        else:
            game = Game.objects.get(slug = game_slug)
            mod = Mod(author = request.user.author, game = game)

    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    
    form = ModForm(request.POST or None, request.FILES or None, instance = mod, is_staff = is_staff)

    if form.is_valid():
        form.save()

        return redirect("view_mod", mod.game.slug, mod.author.user.username, mod.slug)

    return render(request, "mod_submit.html", {"form": form, "game": game})

def show_genres(request):
    return render(request, "genres.html", {'genres': Tag.objects.all()})