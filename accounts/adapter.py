from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin): 
        social_user = sociallogin.user
        if social_user.id:  
            print("alo")
            return          
        try:
            customer = User.objects.get(email=social_user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'
            sociallogin.connect(request, customer)
            user = authenticate(username=customer.username, password=customer.password)
            if user is not None:
                print("Logged in")
                login(request, user)
        except User.DoesNotExist:
            pass