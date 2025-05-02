from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),  # Forgot password page
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),  # Send verification code to email
    path('verify-code/', views.verify_code, name='verify_code'),  # Verify the entered code
    path('reset-password/', views.reset_password, name='reset_password'),
    path('translate/', views.translate_text, name='translate'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('upload/', views.upload, name='upload'),
    # path('output/<str:file_name>/', views.output, name='output'),
    path('output/<str:file_name>/<str:encoded_string>/', views.output, name='output'),
    path('spell_check/', views.spell_check, name='spell_check'),
    path('delete-uploaded-file/', views.delete_uploaded_file, name='delete_uploaded_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)