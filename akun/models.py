from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
# Create your models here.

def getUser(session_key):
    try:
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(pk=uid)
        return user
    except:
        return None
class AccountStatus(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    PILIHAN_KATEGORI=(
        (1,'Super Admin'),
        (2,'HR')
    )
    kategori=models.CharField(max_length=1,default=2)

    def __str__(self):
        return self.user.username

class AccountProfile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    namaPerusahaan=models.CharField(max_length=25, blank=True)
    alamatPerusahaan=models.CharField(max_length=50,blank=True)
    noKontak=models.CharField(max_length=15,blank=True)
    foto=models.ImageField(upload_to='company-profile-picture',default='company-profile-picture/default.png')

    def __str__(self):
        return self.user.username

class AccountLoginAttempt(models.Model):

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    lastLogin=models.TimeField(auto_now=True)

    def __str__(self):
        return self.user.username

class RememberAccount(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    lastSession=models.CharField(max_length=35)
    timeLastSession=models.DateField(auto_now=True,)

    def __str__(self):
        return self.user.username
        
class RequestResetPass(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=32)

    def __str__(self):
        return self.user.username