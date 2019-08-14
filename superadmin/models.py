from django.db import models

# Create your models here.
class TokenDefault(models.Model):

    tokenDefault=models.PositiveIntegerField()
    tanggalDiganti=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tokenDefault

class KategoriSoal(models.Model):
    namaKategori=models.CharField(max_length=50)

    def __str__(self):
        return self.namaKategori

class Soal(models.Model):
    kategori=models.ForeignKey(KategoriSoal,on_delete=models.CASCADE)
    pertanyaan=models.TextField()
    timer=models.IntegerField()

    def __str__(self):
        return self.kategori.kategoriNama

class PilihanJawaban(models.Model):
    soal=models.ForeignKey(Soal,on_delete=models.CASCADE)
    text=models.TextField()
    bobot=models.SmallIntegerField(default=0)

    def __str__(self):
        return "{}-{}".format(self.soal.pertanyaan[:5],self.text[:2])