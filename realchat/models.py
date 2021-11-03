from django.db import models
from user.models import Profile

class DM(models.Model):
    pengundang = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dm_pengundang")
    diundang = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dm_diundang")

    def __str__(self):
      return self.pengundang.name+" - "+self.diundang.name

class Pesan(models.Model):
    dm_id = models.ForeignKey(DM, on_delete=models.CASCADE)
    pengirim = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="pesan_pengirim")
    penerima = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="pesan_penerima")
    isi = models.CharField(max_length=300)
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.isi

