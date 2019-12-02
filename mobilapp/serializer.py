from rest_framework import serializers
from .models import Account,Category,Services,Booking

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username','password')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','user')        

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('name','category','description','image')
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('name','email','location','telephone','time','service')                
                        