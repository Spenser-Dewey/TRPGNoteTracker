import random
import re
import string

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_http_methods, require_safe
from django.forms.models import model_to_dict
from django.views.decorators.clickjacking import xframe_options_exempt

from .models import *
from user_info.models import Player

@require_safe
@login_required
def indexView(request):
    campaign_list = Campaign.objects.all()
    return render(request, "campaign_info/index.html", {'my_campaigns': campaign_list})

@require_safe
@login_required
def campaignView(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    notes = Note.objects.filter(campaign_id = campaign.campaign_id).order_by("-post_date")
    countries = Country.objects.filter(world = campaign.world)
    return render(request, "campaign_info/campaign_view.html", {'campaign': campaign, 'notes': notes, 'country_list': countries})

@login_required
def joinCampaign(request):
    errors = ""
    if request.method == 'POST':
        query_result = list(Campaign.objects.filter(join_code=request.POST['join_code']))
        if len(query_result) == 1: # join codes are enforced by the DB to be unique
            campaign =  query_result[0]
            if len(CampaignRole.objects.filter(campaign=campaign, player=request.user)) == 0:
                CampaignRole.objects.create(campaign=campaign, player=request.user, is_dm=False)
                return redirect('campaign-view', campaign.campaign_id)
            else:
                errors = "You are already part of that campaign"
        else:
            errors = "Campaign Not Found"
    return render(request, "campaign_info/join_campaign.html", {"errors": errors})

@require_safe
@login_required
def manageCampaignView(request, campaign_id):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    participants = CampaignRole.objects.filter(campaign=campaign_id)
    dms = map(lambda role: role.player, participants.filter(is_dm=True))
    players = map(lambda role: role.player, participants.filter(is_dm=False))
    return render(request, "campaign_info/manage_campaign.html", {'campaign': campaign, 'dms': dms, 'players': players })

@require_http_methods(["POST"])
@login_required
def openCampaignView(request, campaign_id, open):
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    if open == "True":
        for _ in range(15):
            try:
                duplicate = False
                campaign.join_code = ''.join(random.choice(string.ascii_uppercase) for i in range(6))
                campaign.save()
            except IntegrityError:
                duplicate = True
            if not duplicate:
                break
        if duplicate:
            error = HttpResponse()
            error.status_code = 500
            error.reason_phrase = "Can't allocate an unused join code to your campaign right now, try again later."
            return error
    else:
        campaign.join_code = ""
        campaign.save()
    return redirect('manage-campaign', campaign_id)

@require_safe
@login_required
def npcView(request, npc_id):
    npc = get_object_or_404(NPC, pk=npc_id)
    campaigns = npc.campaigns.values('pk')
    notes = Note.objects.filter(campaign_id__in = campaigns).filter(note_txt__iregex='\W' + re.escape(npc.name) + '\W').order_by("-post_date")
    return render(request, "campaign_info/npc_info.html", {'npc': npc, 'notes': notes})

@require_safe
@login_required
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

@require_safe
@login_required
@xframe_options_exempt
def countryView(request, world_id, country_id):
    world = get_object_or_404(World, pk=world_id)
    world = model_to_dict(world)
    country = Country.objects.get(pk=country_id)
    # TODO: Have a 'global' Campaign ID that is tracked across user sessions, so we know which campaign to show notes from here
    notes = Note.objects.filter(note_txt__iregex=r'\W' + re.escape(country.name) + '\W').order_by("-post_date")
    url = settings.MEDIA_URL + world["name"] + ".svg"
    return render(request, 'campaign_info/country_map.html', {'world': world, 'map_url': url, "country_name": country.name, "notes": notes})

@require_http_methods(["POST"])
@login_required
def addNotePost(request):
    campaign = Campaign.objects.get(pk=request.POST["campaign_id"])
    newNote = Note(campaign_id=campaign, note_txt=request.POST["note-input"])
    # TODO: Make a NoteForm to validate too long strings
    newNote.save()
    return redirect("campaign-view", campaign.campaign_id)

@require_http_methods(["POST"])
@login_required
def removeNote(request):
    note = Note.objects.get(pk=request.POST["note_id"])
    note.delete()
    return redirect("campaign-view", request.POST["campaign_id"]) 

@require_http_methods(["POST"])
@login_required
def removeNPC(request):
    npc = NPC.objects.get(pk=request.POST["npc_id"])
    if npc is None:
        raise Http404("That NPC does not exist")
    npc.delete()
    return redirect("campaign-view", 1) 

@login_required
def addNPC(request, npc_id=None):
    if npc_id: 
        npc = get_object_or_404(NPC, pk=npc_id)
        initial = {'title':npc.title, 'name': npc.name, 'description_text': npc.description_text,
                        'city': npc.city, 'campaigns': npc.campaigns.values_list('pk', flat=True)}
    else:
        npc = None
        initial = {}
    
    if request.method == 'POST':
        formData = NPCForm(request.POST)
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

@login_required
def createWorld(request):
    error = ''
    if request.method == 'POST':
        formData = WorldForm(request.POST, request.FILES)
        if formData.is_valid():
            # Handle uploaded file in request.FILES
            formData.save(commit=True)
            return redirect('create-campaign')
    return render(request, 'campaign_info/create_world.html', {'form': WorldForm(), 'error': error})

@login_required
def createCampaign(request):
    if request.method == 'POST':
        formData = CampaignForm(request.POST)
        if(formData.is_valid()):
            campaign = formData.save(commit=True)
            CampaignRole.objects.create(campaign=campaign, player=request.user, is_dm=True)
            return redirect('campaign-view', campaign.campaign_id)
        else:
            print("INVALID FORM")
    return render(request, 'campaign_info/create_campaign.html', {'form': CampaignForm()})

@require_http_methods(["POST"])
@login_required
def deleteCampaign(request):
    campaign = Campaign.objects.get(pk=request.POST["campaign_id"])
    campaign.delete()
    return redirect("account") 