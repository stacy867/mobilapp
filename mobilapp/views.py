from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .email import send_welcome_email
from mobilapp.forms import RegistrationForm,AccountAuthenticationForm,NewServiceForm,NewBookingForm,CompanyProfileForm,CommentForm,UserProfileForm
from mobilapp.models import Account,Category,Services,Booking,Comment,CompanyProfile,UserProfile
from django.http import JsonResponse,HttpResponseRedirect


from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .permissions import IsAuthenticatedOrReadOnly


from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import AccountSerializer,CategorySerializer,BookingSerializer
from rest_framework import status



class AccountList(APIView):
    def get(self, request, format=None):
        all_accounts = Account.objects.all()
        serializers = AccountSerializer(all_accounts, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = AccountSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryList(APIView):
    def get(self, request, format=None):
        all_categories = Category.objects.all()
        serializers = CategorySerializer(all_categories, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = CategorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookingList(APIView):
    def get(self, request, format=None):
        all_bookings = Booking.objects.all()
        serializers = BookingSerializer(all_bookings, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
        serializers = BookingSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)    
    

    
# Create your views here.
# @login_required(login_url='register/')
def welcome(request):
  # context ={}
  accounts=Account.objects.all()
  categories=Category.objects.all()
  form = NewBookingForm()
 
  return render(request,'index.html',{"accounts":accounts,"categories":categories,"bookingForm": form})

def logout_view(request):
	logout(request)
	return redirect('/')

def login_view(request):

	context = {}

	# user = request.user
	# if user.is_authenticated: 
	# 	return redirect("welcome")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("welcome")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "registration/login.html", context)

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('welcome')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request,'registration/registration_form.html', context)

@login_required
def new_service(request):
    current_user = request.user
    companyprofile=CompanyProfile.objects.filter(user=current_user).first()
    if request.method == 'POST':
        form = NewServiceForm(request.POST,request.FILES)
        if form.is_valid():
            print("cgfjhk")
            s_post = form.save(commit=False)
            s_post.companyprofile = companyprofile
            s_post.save()
        return redirect('all-services')
    else:
        form = NewServiceForm()
    return render(request,'new_service.html',{"form": form})

def all_services(request):
    services=Services.objects.all()	
    return render(request,'all_services.html',{"services":services})	

	
def service(request,category_id):
	categories=Category.objects.get(id=category_id)
	services = Services.objects.filter(category=categories.id).all().prefetch_related('comment_set')
 
	comment = Comment.objects.filter(service=services).all()
	form = NewBookingForm()
	print(services)
	return render(request,'service.html',{"services":services,"category_id":category_id,"bookingForm":form})

@login_required
def new_booking(request):
        
        current_user = request.user
        if request.method == 'POST':
            form = NewBookingForm(request.POST,request.FILES)
            if form.is_valid():
                print("cgfjhk")
               
                userprofile = form.cleaned_data['userprofile']
                telephone = form.cleaned_data['telephone']
                location = form.cleaned_data['location']
                time = form.cleaned_data['time']
                service = form.cleaned_data['service']
                email = form.cleaned_data['email']

                recipient = Booking(userprofile = userprofile,telephone=telephone,location=location,time=time,service=service,email=email)
                recipient.user=current_user
                recipient.save()
                send_welcome_email(userprofile,email)
    
                return redirect('user-profile')
    

        else:
            form = NewBookingForm()
        return render(request,'new_booking.html',{"form": form,"current_user":current_user})
 		
	

def search_results(request):
    # print("searched_images")
    if 'service' in request.GET and request.GET["service"]:
        search_term = request.GET.get("service")
        searched_service = Services.search_by_name(search_term)
        print("searched_service")
        message = f"{search_term}"

        return render(request, 'all_apps/search.html',{"message":message,"services": searched_service})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all_apps/search.html',{"message":message})



def new_comment(request):

    current_user = request.user
    service = Services.objects.all()
    # companyprofile = CompanyProfile.objects.all()
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            # comment.service = service
            comment.save()
            return redirect('welcome')

    else:
        form = CommentForm()
    return render(request, 'new_comment.html', {"form": form, "service": service})


def comment(request, service_id):
    try:
        comment = Comment.objects.get(id=service_id).all()
    except DoesNotExist:
        raise Http404()
    return render(request, "all_apps/profiledisplay.html", {"comment": comment})

@login_required
def companyprofile_form(request):
    current_user = request.user
    profile = CompanyProfile.objects.filter(user=current_user).first()
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('profiledisplay')

    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'registration/profile.html', {"form": form})

@login_required
def userprofile_form(request):
    current_user = request.user
    profile = UserProfile.objects.filter(user=current_user).first()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
        return redirect('user-profile')

    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'registration/userform.html', {"form": form})    


@login_required
def company_profile(request):
    current_user = request.user
    company_name = CompanyProfile.objects.filter(user=current_user.id).first()
    service1=Services.objects.filter(companyprofile=company_name).all().prefetch_related('booking_set')
    # booking=Booking.objects.get(service=service1.id).all()
    # complete_task=Booking.objects.filter(user=current_user.id).update(complete =True)
    
    message=None
    if  company_name is None:
        message="you are not registered as a business"
    elif company_name.approved == False:
         message="check in 2 hrs"
    else:
        message="Welcome to your dashboard"
   
    comment = Comment.objects.all()
    
   

    return render(request, 'all_apps/profiledisplay.html', {"company_name": company_name,"complete_task":complete_task, "current_user": current_user, "comment": comment,"message":message,"service1":service1})

@login_required
def user_profile(request):
    current_user = request.user
    bookings=Booking.objects.filter(user=current_user.id).all()
    profile = UserProfile.objects.filter(user=current_user).first()
    
    return render(request,'all_apps/userprofile.html',{"bookings":bookings,"current_user":current_user,"profile":profile})

@login_required
def complete_task(request):
    current_user = request.user
    
    complete_task=Booking.objects.filter(user=current_user.id).update(complete =True)
   
    
    return redirect("user-profile")

    
        