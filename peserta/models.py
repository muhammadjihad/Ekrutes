from django.db import models

# Create your models here.

class BiodataPeserta(models.Model):

    namaDepan=models.CharField(max_length=20)
    namaBelakang=models.CharField(max_length=20)
    PILIHAN_JENIS_KELAMIN=(
        (0,"Perempuan"),
        (1,"Laki - Laki")
    )
    jenisKelamin=models.PositiveSmallIntegerField()
    tanggalLahir=models.DateField()
    noKontak=models.CharField(max_length=13)
    email=models.EmailField()
    tanggalRegistrasi=models.DateField()
    status=models.SmallIntegerField()
    skor=models.IntegerField(default=0)
    lulus=models.BooleanField(default=False)

    def __str__(self):
        return self.namaDepan

