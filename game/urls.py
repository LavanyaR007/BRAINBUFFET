from django.urls import path
from django.urls import path,include
from . import views
#from game.Graphs import SimpleExample

urlpatterns = [
    path('allgames', views.allgames, name='allgames'),
    path('hangman', views.hangman, name='hangman'),
    path('pixelart',views.pixelart,name='pixelart'),
    path('memorycard',views.memorycardgame,name='memorycard'),
    path('memoryanalysis',views.memory_game_analysis,name='memoryanalysis'),
    path('flagmatcher',views.flagmatchergame,name='flagmatcher'),
    path('numberpuzzle',views.numberpuzzle,name="numberpuzzle"),
    path('simon',views.simongame,name='simon'),
    path('hitthecat',views.hitthecatgame,name='hitthecat'),
    path('mathquizgame',views.mathquizgame,name='mathquiz'),
    #path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('simongameanalysis',views.memory_score_graph,name='simongameanalysis')
]