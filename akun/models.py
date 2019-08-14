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


class Kecamatan(models.Model):
    id_kecamatan = models.SmallIntegerField(primary_key=True)
    f_id_kota = models.SmallIntegerField()
    nama_kecamatan = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'kecamatan'


class Kota(models.Model):
    id_kota = models.SmallIntegerField(primary_key=True)
    f_id_prov = models.IntegerField()
    nama_kota = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'kota'

class AccountProfile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE)
    namaPerusahaan=models.CharField(max_length=25, blank=True)
    PILIHAN_KATEGORI=(
        (1,'Super Admin'),
        (2,'HR')
    )
    kategori=models.CharField(max_length=1,default=2)
    alamatPerusahaan=models.CharField(max_length=50,blank=True)
    noKontak=models.CharField(max_length=15,blank=True)
    person=models.CharField(max_length=30)
    tokenTest=models.IntegerField(default=50)
    PILIHAN_JENIS_AKUN=(
        (0,'Demo'),
        (1,'Premium')
    )
    tanggalRegistrasi=models.DateField(auto_now_add=True)
    jenisAkun=models.SmallIntegerField(choices=PILIHAN_JENIS_AKUN,default=0)
    foto=models.ImageField(upload_to='company-profile-picture',default='company-profile-picture/default.png')
    npwp=models.CharField(max_length=23,blank=True)
    idKecamatan=models.ForeignKey(Kecamatan,on_delete=models.CASCADE,blank=True,null=True)
    deskripsi=models.TextField(blank=True)
    flag=models.BooleanField(default=True)

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