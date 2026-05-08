from django.db import models

# Create your models here.
class Formulario(models.Model):

    kobo_id = models.IntegerField(unique=True, null=True)

    uuid = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    data_envio = models.DateTimeField(
        null=True,
        blank=True
    )

    nome = models.CharField(max_length=80)
    idade = models.IntegerField()
    hobbie = models.CharField(max_length=200)
    gosta_chocolate = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
