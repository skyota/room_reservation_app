from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomeView, RoomView, ReservationListView, ReservationAddView, ReservationDeleteView

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('room/<int:pk>/', login_required(RoomView.as_view()), name='room'),
    path('room/<int:pk>/add_reservation/', login_required(ReservationAddView.as_view()), name='add_reservation'),
    path('room/<int:pk>/list/', login_required(ReservationListView.as_view()), name='get_reservations'),
    path('room/<int:pk>/reservation/<int:reservation_id>/delete/', login_required(ReservationDeleteView.as_view()), name='delete_reservation'),
]
