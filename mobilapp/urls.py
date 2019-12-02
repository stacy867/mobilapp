from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from mobilapp.views import registration_view

urlpatterns=[

    url('^$',views.welcome,name = 'welcome'),
    url(r'^newservice/(?P<category_id>\d+)',views.new_service,name = 'new-service'),
    url(r'^newbooking/',views.new_booking,name = 'new-booking'),
    url(r'^service/(?P<category_id>\d+)',views.service,name = 'service'),
    url(r'^search/',views.search_results,name = 'search'),
    url(r'^account/profileform', views.profile_form, name='profile'),
    url(r'^account/profiledisplay', views.company_profile, name='profiledisplay'),
    url(r'^new/comment/', views.new_comment, name='new-comment'),
    url(r'^comment/(?P<service_id>\d+)', views.comment, name='comment'),
 

    url(r'login/',views.login_view,name = 'login'),
    url(r'register/',views.registration_view,name = 'register'),
    url(r'logout/',views.logout_view,name = 'logout'),
    url(r'^api/account/$', views.AccountList.as_view(),name='accounts-api'),
    url(r'^api/category/$', views.CategoryList.as_view(),name='category-api'),
    url(r'^api/booking/$', views.BookingList.as_view(),name='booking-api')

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
