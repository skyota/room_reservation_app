import json
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404, HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, redirect

from .models import Room, Reservation
from .forms import ReservationForm, CalendarForm

class HomeView(ListView):
    model = Room
    template_name = 'reservation/home.html'
    
class RoomView(DetailView):
    model = Room
    template_name = 'reservation/room.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_list = Room.objects.all()
        context.update({
            'room_list': room_list,
            'csrf_token': get_token(self.request),
        })
        return context

def add_reservation(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get("title")
            username = data.get("username")
            laboratory = data.get("laboratory")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            
            if not title or not start_date or not end_date:
                raise Http404("不正なデータです")
            
            reservation = Reservation(
                title = title,
                username = username,
                laboratory = laboratory,
                start_time = start_date,
                end_time = end_date,
                room_id=pk,
                user=request.user
            )
            reservation.save()
            
            return JsonResponse({
                'id': reservation.id,
                'title': reservation.title,
                'username': reservation.username,
                'laboratory': reservation.laboratory,
                'start': reservation.start_time,
                'end': reservation.end_time,
            })
        
        except json.JSONDecodeError:
            raise Http404("データの読み込みに失敗しました。")
    
    else:
        raise Http404()
    
def get_reservations(request, pk):
    if request.method == "GET":
        room = get_object_or_404(Room, pk=pk)
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if not start_date or not end_date:
            raise Http404("開始日または終了日が指定されていません")

        reservations = Reservation.objects.filter(
            room=room,
            user=request.user,
            start_time__lt=end_date,
            end_time__gt=start_date
        )

        events = []
        for reservation in reservations:
            events.append({
                "id": reservation.id,
                "title": reservation.title,
                "username": reservation.username,
                "laboratory": reservation.laboratory,
                "start": reservation.start_time.isoformat(),
                "end": reservation.end_time.isoformat(),
            })

        return JsonResponse(events, safe=False)

    raise Http404("不正なリクエストです")

def reservation_detail(request, pk, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)

    return render(request, 'reservation/reservation_detail.html', {
        'reservation': reservation,
    })
    
def delete_reservation(request, pk, reservation_id):
    if request.method == "DELETE":
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
        return JsonResponse({"message": "予約が削除されました"}, status=200)
    
    raise Http404("不正なリクエストです")
