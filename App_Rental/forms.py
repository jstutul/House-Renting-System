from django import forms
from App_Rental.models import House, HouseImage

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['description']       
     
