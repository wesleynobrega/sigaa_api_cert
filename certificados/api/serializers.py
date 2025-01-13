from rest_framework import serializers
from certificados.models import Alunos, Cursos, Turmas


class AlunoSerializer(serializers.ModelSerializer):
    """ Serializer for Alunos model """
    class Meta:
        model = Alunos
        fields = '__all__'


class AlunoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alunos
        fields = ['nome', 'cpf', 'data_de_nascimento',
                  'email', 'telefone', 'matricula']

    def validate_cpf(self, value):
        if value and Alunos.objects.filter(cpf=value).exists():
            raise serializers.ValidationError("Este CPF já está em uso.")
        return value

    def validate_telefone(self, value):
        if value and Alunos.objects.filter(telefone=value).exists():
            raise serializers.ValidationError("Este telefone já está em uso.")
        return value

    def validate_email(self, value):
        if value:
            if '@' not in value:
                raise serializers.ValidationError("Formato de email inválido.")
        return value

    def validate_matricula(self, value):
        if value and value <= 0:
            raise serializers.ValidationError(
                "A matrícula deve ser um número positivo.")
        return value


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = '__all__'


class CursoCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cursos
        fields = ['nome_do_curso', 'area_curso']

    def validate_nome_do_curso(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "O nome do curso deve ter pelo menos 3 caracteres.")
        return value

    def validate_area_curso(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "A área do curso deve ter pelo menos 3 caracteres.")
        return value


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turmas
        fields = '__all__'


class TurmaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turmas
        fields = ['nome_da_turma', 'data_inicio', 'data_fim',
                  'data_aprovado_registro', 'data_liberacao_certificado']

    def validate(self, data):
        if data['data_inicio'] >= data['data_fim']:
            raise serializers.ValidationError(
                "A data de início deve ser anterior à data de fim.")
        if data['data_fim'] > data['data_liberacao_certificado']:
            raise serializers.ValidationError(
                "A data de liberação do certificado deve ser posterior à data de fim.")
        return data

    def validate_nome_da_turma(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "O nome da turma deve ter pelo menos 3 caracteres.")


class CertificadoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(max_length=255)
    curso = serializers.CharField(max_length=255)
    data_emissao = serializers.DateField()
    email = serializers.EmailField()
