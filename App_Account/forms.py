# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from App_Account.models import UserProfile, USER_TYPE_LIST

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=USER_TYPE_LIST,required=True,widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'user_type')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'password1':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Password'})
            elif field_name == 'password2':
                field.widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
            elif isinstance(field.widget, forms.Select):  # Check if the widget is a Select widget
                field.widget.attrs.update({'class': 'form-control form-select',  'required': 'required','placeholder':  field_name.replace('_', ' ').capitalize()})
            else:
                field.widget.attrs.update({'class': 'form-control',  'required': 'required','placeholder': field_name.replace('_', ' ').capitalize()})
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        user_type = cleaned_data.get("user_type")
        if user_type == '0':
            self.add_error('user_type', 'Please select a user type.')
        return cleaned_data
