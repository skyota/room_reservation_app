from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Room

class HomeView(ListView):
    model = Room
    template_name = 'reservation/home.html'
    
class RoomView(TemplateView):
    template_name = 'reservation/room.html'
