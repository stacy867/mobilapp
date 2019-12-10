from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account,Services,Booking,CompanyProfile,Comment,UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', )


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")



class NewServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name','description','location','category','image']

class NewBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude=['user']
        fields = ['userprofile','telephone','location','time','service','email']

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        exclude=['approved']
        fields = ['name', 'email','location']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude=['service','user']
        fields = ['name', 'telephone','location']        
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','feedback','service','companyprofile']      
