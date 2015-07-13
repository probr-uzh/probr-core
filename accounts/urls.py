from views import UserMeView
from django.conf.urls import url


urlpatterns = [

    ### Endpoints accessed by frontend  ###

    #details of a device by uuid
    url(r'^api/users/me/+$', UserMeView.as_view(), name='user-me'),

]