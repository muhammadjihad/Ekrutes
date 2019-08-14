from django.db import models
from akun.models import AccountProfile
from superadmin.models import KategoriSoal
from akun.models import AccountProfile
from peserta.models import BiodataPeserta
# Create your models here.

class Sesi(models.Model):

    namaSesi=models.CharField(max_length=255)
    deskripsi=models.TextField()
    user=models.ForeignKey(AccountProfile,on_delete=models.CASCADE)
    kodeSesi=models.CharField(max_length=5)
    tanggalBukaSesi=models.DateTimeField(auto_now_add=True)
    jamMulai=models.DateTimeField()
    jamSelesai=models.DateTimeField()
    totalPeserta=models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.user.namaPerusahaan,self.namaSesi)

class Jawaban(models.Model):

    peserta=models.ForeignKey(BiodataPeserta,on_delete=models.CASCADE)
    sesi=models.ForeignKey(Sesi,on_delete=models.CASCADE)
    pilihan=models.SmallIntegerField(blank=True,null=True)
    bobotPilihan=models.SmallIntegerField(blank=True,default=0)

    def __str__(self):
        return "{} - {}".format(self.sesi.namaSesi,self.peserta.namaDepan)