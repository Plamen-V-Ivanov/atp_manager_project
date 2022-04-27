from django.urls import path

from atp_manager.auth_app.views import UserLoginView, ProfileDetailsView, AddProfileView, \
    logout_user, DeleteProfileFormView

urlpatterns = (
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', logout_user, name='logout user'),
    path('<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('add/', AddProfileView.as_view(), name='add a profile'),
    path('delete/', DeleteProfileFormView.as_view(), name='delete a profile'),
    # path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete a profile'),
    # path('delete/', DeleteProfileView.as_view(), name='delete a profile'),
)
