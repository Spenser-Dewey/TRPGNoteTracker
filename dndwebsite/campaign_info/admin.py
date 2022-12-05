from django.contrib import admin

from .models import Campaign, Character, Country, City, NPC, World, Note

admin.site.register(World)
admin.site.register(Campaign)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(NPC)
admin.site.register(Character)
admin.site.register(Note)

