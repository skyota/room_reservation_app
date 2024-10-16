import json
from django.views.generic.detail import DetailView, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import Room, Reservation

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
    
class ReservationListView(View):
    def get(self, request, pk):
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

        events = [
            {
                "id": reservation.id,
                "title": reservation.title,
                "username": reservation.username,
                "laboratory": reservation.laboratory,
                "start": reservation.start_time.isoformat(),
                "end": reservation.end_time.isoformat(),
            } for reservation in reservations
        ]

        return JsonResponse(events, safe=False)

class ReservationAddView(View):
    def post(self, request, pk):
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
                title=title,
                username=username,
                laboratory=laboratory,
                start_time=start_date,
                end_time=end_date,
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
        except Exception as e:
            raise Http404(f"エラーが発生しました: {str(e)}")

class ReservationDeleteView(View):
    def delete(self, request, pk, reservation_id):
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        reservation.delete()
        return JsonResponse({"message": "予約が削除されました"}, status=200)

class RoomAddView(CreateView):
    model = Room
    template_name = 'reservation/add_room.html'
    fields = ['name']
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        return super().form_valid(form)

class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'reservation/room_confirm_delete.html'
    success_url = reverse_lazy('home')     
