from django import forms
from App_Rental.models import House, HouseImage,HouseComment

class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['description']       
     
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={
        'class':'form-control',
        'id':'comm',
        'rows':3,
        'cols':40,
        'padding':'10px',
        'placeholder':"Enter  your Text here",
    }))
    class Meta:
        model = HouseComment
        fields = ['content']