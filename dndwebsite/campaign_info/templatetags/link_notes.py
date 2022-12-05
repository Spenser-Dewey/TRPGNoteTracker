from ..models import NPC, City, Country
from ..util import replaceAllWithUrl
from django.utils.html import escape
from django import template

register = template.Library()

@register.filter(name='link')
def addTextWithLinks(passedNote):
    """ Adds links to the text of a note, linking npc names, countries, and cities to their own pages. """
    linkedText = escape(passedNote.note_txt)
    npcNames = NPC.objects.filter(campaigns=passedNote.campaign_id).values_list('name', 'npc_id')
    cityNames = City.objects.filter(country__world=passedNote.campaign_id.world).values_list('name', 'country__world_id', 'country_id')
    countryNames = Country.objects.filter(world=passedNote.campaign_id.world).values_list('name', 'world_id', 'country_id')

    linkedText = replaceAllWithUrl(linkedText, npcNames, 'npc-view')
    linkedText = replaceAllWithUrl(linkedText, cityNames, 'country-map')
    linkedText = replaceAllWithUrl(linkedText, countryNames, 'country-map')

    return linkedText