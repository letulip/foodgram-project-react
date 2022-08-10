from django.contrib import admin
from .models import Tag, Favorites, Recipe, Ingredient, IngredsAmount

admin.site.register(Tag)
admin.site.register(Favorites)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredsAmount)
