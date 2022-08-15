from django.contrib import admin

from .models import Favorite, Ingredient, IngredientsAmount, Recipe, Tag

admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(IngredientsAmount)
