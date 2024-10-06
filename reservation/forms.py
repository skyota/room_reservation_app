from django import forms


class ReservationForm(forms.Form):
    title = forms.CharField(required=True, max_length=32)
    start_time = forms.IntegerField(required=True)
    end_time = forms.IntegerField(required=True)
    
class CalendarForm(forms.Form):
    start_time = forms.IntegerField(required=True)
    end_time = forms.IntegerField(required=True)
