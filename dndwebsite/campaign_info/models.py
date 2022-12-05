from django.db import models
from django.db.models.fields import AutoField
from django.forms import widgets
from django.forms.models import ModelForm
from django.utils import timezone
from django.utils.translation import gettext_lazy

# World/Universe that campaigns take place in
class World(models.Model):
    world_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# A campaign that Players participate in, through Characters (non-NPC)
class Campaign(models.Model):
    campaign_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    world = models.ForeignKey(World, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

# A Country on a World
class Country(models.Model):
    country_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    world = models.ForeignKey(World, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# A City in a Country. In a city-state, this would be a country with the same name
class City(models.Model):
    city_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name + ", located in " + self.country.__str__()

# A non-player character
class NPC(models.Model):
    npc_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    description_text = models.CharField(max_length=200)
    title = models.CharField(max_length=16, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    campaigns = models.ManyToManyField(Campaign, blank=True)

    def __str__(self):
        return self.title + " " + self.name + " of " + self.city.__str__()

class NPCForm(ModelForm):
    class Meta:
        model = NPC
        fields = ['title', 'name', 'description_text', 'city', 'campaigns']
        widgets = {
            'description_text': widgets.Textarea(attrs={'cols':80, 'rows': 3}) 
        }
        labels = {
            'city': gettext_lazy('City of origin, or home city'),
        }
        help_texts = {
            'title': gettext_lazy('For instance, lord, lady, mr., etc.'),
        }

# A player character
class Character(models.Model):
    character_id = AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    str_attr = models.SmallIntegerField()
    dex_attr = models.SmallIntegerField()
    con_attr = models.SmallIntegerField()
    wis_attr = models.SmallIntegerField()
    int_attr = models.SmallIntegerField()
    cha_attr = models.SmallIntegerField()
    campaign = models.ForeignKey(Campaign, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

# A player's note about a particular campaign
class Note(models.Model):
    note_id = AutoField(primary_key=True)
    campaign_id = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    note_txt = models.CharField(max_length=512)
    post_date = models.DateTimeField(default=timezone.now)
    
    def contains(self, search_string):
        return search_string in self.note_txt
    