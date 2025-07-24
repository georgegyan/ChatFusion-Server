from django.template.loader import render_to_string  
from django.utils.crypto import get_random_string  
from django.utils import timezone  
from templated_mail.mail import BaseEmailMessage  

def send_verification_email(user):  
    token = get_random_string(length=32)  
    user.verification_token = token  
    user.verification_sent_at = timezone.now()  
    user.save()  

    context = {  
        'user': user,  
        'token': token,  
        'expiry_days': 3  
    }  

    email = BaseEmailMessage(  
        template_name='email/verification.html',  
        context=context  
    )  
    email.send([user.email])  