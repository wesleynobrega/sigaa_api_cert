from django.db import models

# Create your models here.


class Alunos(models.Model):
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=15)
    data_de_nascimento = models.DateField()
    email = models.CharField(max_length=255)
    telefone = models.CharField(max_length=18)
    matricula = models.BigIntegerField()
    
class Cursos(models.Model):
    nome_do_curso = models.CharField(max_length=50)
    area_curso = models.CharField(max_length=50)   

class Turmas(models.Model):
    nome_da_turma = models.CharField(max_length=255)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    data_aprovado_registro = models.DateField()
    data_liberacao_certificado = models.DateField()



