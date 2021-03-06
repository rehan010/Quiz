from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^accounts/profile/$', views.UserProfileView.as_view(), name="profile"),
    url(r'^accounts/quiz/$', views.UserQuizView.as_view(), name="quiz"),
    url(r'^accounts/status/$', views.UserStatusView.as_view(), name="status"),
]
