from django.urls import path
from . import views
app_name='account'
urlpatterns=[
    path('register/', views.UserRegistration.as_view(),name= 'register_user'),
    path('login/', views.UserLoginView.as_view(), name='login_user'),
    path('logout/', views.UserLogout.as_view(),name= 'logout_user'),
    path('profile/<int:user_id>', views.ProfileUserView.as_view(),name= 'profile_user'),
    path('reset/',views.UserPasswordResetView.as_view(),name='password_reset'),
    path('reset/done',views.UserPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('confirm/<uidb64>/<token>',views.UserPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('confirm/complete',views.UserPasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('follow/<int:user_id>',views.UserFollow.as_view(),name="user_follow"),
    path('unfollow/<int:user_id>',views.UserUnFollow.as_view(),name="user_unfollow"),

    path('editprofile/',views.EditUserView.as_view(),name='edit_profile')
]