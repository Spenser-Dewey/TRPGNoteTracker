from django.conf import settings
from django.urls import reverse
from django.http.response import Http404
from django.shortcuts import redirect, get_object_or_404, render
from .models import Campaign, NPC, NPCForm, World, Note, Country
from django.forms.models import model_to_dict
from django.views.decorators.clickjacking import xframe_options_exempt
import re


def indexView(request):
    campaign_list = Campaign.objects.all()
    return render(request, "campaign_info/index.html", {'my_campaigns': campaign_list})

def campaignView(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    notes = Note.objects.filter(campaign_id = campaign.campaign_id).order_by("-post_date")
    countries = Country.objects.filter(world = campaign.world)
    return render(request, "campaign_info/campaign_view.html", {'campaign': campaign, 'notes': notes, 'country_list': countries })

def npcView(request, npc_id):
    npc = get_object_or_404(NPC, pk=npc_id)
    campaigns = npc.campaigns.values('pk')
    notes = Note.objects.filter(campaign_id__in = campaigns).filter(note_txt__iregex='\W' + re.escape(npc.name) + '\W').order_by("-post_date")
    return render(request, "campaign_info/npc_info.html", {'npc': npc, 'notes': notes})

@xframe_options_exempt
def worldView(request, world_id):
    world = get_object_or_404(World, pk=world_id)
    world = model_to_dict(world)
    countries = Country.objects.filter(world = world_id)
    url = settings.MEDIA_URL + world["name"] + ".svg"
    country_urls = []
    for country in countries:
        country_urls.append(reverse("country-map", kwargs={"world_id": world_id, "country_id": country.country_id}))
    countries = list(countries.values_list('name', flat=True))
    return render(request, 'campaign_info/world_map.html', {'world': world, 'map_url': url, "country_map":  dict(zip(countries, country_urls))})

@xframe_options_exempt
def countryView(request, world_id, country_id):
    world = get_object_or_404(World, pk=world_id)
    world = model_to_dict(world)
    country = Country.objects.get(pk=country_id)
    # TODO: Have a 'global' Campaign ID that is tracked across user sessions, so we know which campaign to show notes from here
    notes = Note.objects.filter(note_txt__iregex=r'\W' + re.escape(country.name) + '\W').order_by("-post_date")
    url = settings.MEDIA_URL + world["name"] + ".svg"
    return render(request, 'campaign_info/country_map.html', {'world': world, 'map_url': url, "country_name": country.name, "notes": notes})

def addNotePost(request):
    if request.method == 'POST':
        campaign = Campaign.objects.get(pk=request.POST["campaign_id"])
        newNote = Note(campaign_id=campaign, note_txt=request.POST["note-input"])
        # TODO: Make a NoteForm to validate too long strings
        newNote.save()
        return redirect("campaign-view", campaign.campaign_id)
    return redirect("index")

def removeNote(request):
    if request.method == 'POST':
        note = Note.objects.get(pk=request.POST["note_id"])
        note.delete()
        return redirect("campaign-view", 1) 
    else:
        return redirect("index")

def removeNPC(request):
    if request.method == 'POST':
        npc = NPC.objects.get(pk=request.POST["npc_id"])
        if npc is None:
            raise Http404("That NPC does not exist")
        npc.delete()
        return redirect("campaign-view", 1) 
    else:
        return redirect("index")

def addNPC(request, npc_id=None):
    if npc_id: 
        npc = get_object_or_404(NPC, pk=npc_id)
        initial = {'title':npc.title, 'name': npc.name, 'description_text': npc.description_text,
                        'city': npc.city, 'campaigns': npc.campaigns.values_list('pk', flat=True)}
    else:
        npc = None
        initial = {}
    
    if request.method == 'POST':
        formData = NPCForm(request.POST, request.FILES)
        if(formData.is_valid()):
            npc = formData.save(commit=False)
            if npc_id:
                npc.npc_id = npc_id
            npc.save()
            formData.save(commit=True)
            return redirect('npc-view', npc.npc_id)
        else:
            print("INVALID FORM")
    return render(request, 'campaign_info/add_npc.html', {'form': NPCForm(initial=initial, instance=npc), 'npc_id': npc_id})