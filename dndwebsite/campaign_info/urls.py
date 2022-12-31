from django.urls import path

from . import views

urlpatterns = [
    path('campaign-view/', views.indexView, name='view-campaigns'),
    path('campaign-view/create/', views.createCampaign, name='create-campaign'),
    path('campaign-view/delete/', views.deleteCampaign, name='delete-campaign'),
    path('campaign-view/<int:campaign_id>/', views.campaignView, name='campaign-view'),
    path('campaign-view/add-note/', views.addNotePost, name='add-note'),
    path('campaign-view/remove-note/', views.removeNote, name='remove-note'),
    path('campaign-view/remove-npc/', views.removeNPC, name='remove-npc'),
    path('npc-view/<int:npc_id>/', views.npcView, name='npc-view'),
    path('world-map/create/', views.createWorld, name='create-world'),
    path('world-map/<int:world_id>/', views.worldView, name='world-map'),
    path('world-map/<int:world_id>/<int:country_id>', views.countryView, name='country-map'),
    path('update-npc/<int:npc_id>', views.addNPC, name='update-npc'),
    path('update-npc', views.addNPC, name='add-npc')
]