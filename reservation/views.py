from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Room

class HomeView(ListView):
    model = Room
    template_name = 'reservation/home.html'
    
class RoomView(DetailView):
    model = Room
    template_name = 'reservation/room.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_list = Room.objects.all()
        context.update({'room_list': room_list})
        return context
