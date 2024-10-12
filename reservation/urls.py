from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import HomeView, RoomView, add_reservation, ReservationListView, delete_reservation

urlpatterns = [
    path('', login_required(HomeView.as_view()), name='home'),
    path('room/<int:pk>/', login_required(RoomView.as_view()), name='room'),
    path('room/<int:pk>/add_reservation/', login_required(add_reservation), name='add_reservation'),
    path('room/<int:pk>/list/', login_required(ReservationListView.as_view()), name='get_reservations'),
    path('room/<int:pk>/reservation/<int:reservation_id>/delete/', login_required(delete_reservation), name='delete_reservation'),
]
