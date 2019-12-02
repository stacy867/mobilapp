from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


# Create your models here.
class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser,models.Model):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email
		
		

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	def get_short_name(self):
		return self.username

class Category(models.Model):
	name=models.CharField(max_length=50)
	user=models.ForeignKey('Account',on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/')	
	
    
	def __str__(self):
		return self.name
		@classmethod
		def find_category(cls,category_id):
			category = cls.objects.get(id=category_id)
			return category		


class Services(models.Model):
	name=models.CharField(max_length=70)
	category=models.ForeignKey(Category,on_delete=models.CASCADE)
	description=models.CharField(max_length=250)
	# companyprofile=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
	location=models.SlugField(max_length=500)
	image = models.ImageField(upload_to='images/')

	

	def save_services(self):
		self.save()		
        
	@classmethod
	def find_category(cls,category_id):
		category=category.id
		category1 = cls.objects.get(category=category_id)
		return category1

	@classmethod
	def search_by_name(cls,service):
		certain_service = cls.objects.filter(name__icontains=service)
		return certain_service
	def __str__(self):
		return self.name			

class Booking(models.Model):
	name=models.CharField(max_length=100)
	telephone=models.IntegerField()
	email=models.EmailField(max_length=70)
	location=models.SlugField(max_length=100)
	time=models.DateTimeField()
	# category=models.ForeignKey(Category,on_delete=models.CASCADE)
	service=models.ForeignKey(Services,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

		@classmethod
		def find_service(cls,service_id):
			service=service.id
			service1 = cls.objects.get(service=service_id)
			return service1							

        
class CompanyProfile(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=250)
    location = models.SlugField(max_length=500)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

        @classmethod
        def find_category(cls, category_id):
            category = category.id
            category1 = cls.objects.get(category=category_id)
            return category1 
        
class Comment(models.Model):
    feedback = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    companyprofile = models.ForeignKey(
        CompanyProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)

    def __str__(self):
        return self.feedback

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    def update_comment(self):
        self.update()               



	
	