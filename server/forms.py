from .models import User

class CustomUserCreationForm():

    class Meta():
        model = User
        fields = fields = ['fb_id', 'fb_name', 'fb_token', 'fb_token_exp', 'email', 'telephone', 'birth_date']