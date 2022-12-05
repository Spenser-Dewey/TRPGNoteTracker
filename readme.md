# DND Note Website


## TODO modifications

So we want support for a few extra things here, and adjust some existing features to make this easier to use.

### Known bugs
  * Linking notes doesn't work on first/last word
  * Deleting NPC button appears broken

### Desired adjustments:
  * Ability to edit notes
  * Display NPC sidebar in the NPC add/edit views
  * Fix the back button to actually navigate back
  * Replace the (stub) character sheet button with naviagation back to main campaign view
  * Add searching to 

### New Features (ordered by size desc)
  1) Model additions
      1) Create 'organizations' that characters can belong to
      2) Create 'families' that characters can belong to
      3) New 'Event' type, which can have multiple notes associated. Notes can only associate with one event
      4) Incorporate time into events
      5) Split NPC description up to include race and gender slots, approx. age
  2) View additions
      1) Update NPC edit form to include new information breakdowns.
      2) Add optional city view (Ask peter about city maps once feature complete)
      3) Related to Model points 1-2, create a new view specifically to view organizations/families
      4) Related to Model point 3, create a new view specifically to view Events, or add filtering to main notes view
  3) General additions
     1) Importance field in NPC lists, so I can sort NPCs
     2) Add user sessions
        1) Includes log-in screen
        2) Give access to some campaigns for some users, each campaign has a ~DM~ role
        3) Associate notes with users  
     3) Calendar!
