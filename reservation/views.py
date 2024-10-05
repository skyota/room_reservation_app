from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'reservation/home.html'
    
class RoomView(TemplateView):
    template_name = 'reservation/room.html'
