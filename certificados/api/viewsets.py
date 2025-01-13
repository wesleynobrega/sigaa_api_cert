from rest_framework import viewsets, filters, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from certificados.models import Alunos, Cursos, Turmas
from .serializers import (
    AlunoSerializer, AlunoCreateUpdateSerializer,
    CursoSerializer, CursoCreateUpdateSerializer,
    TurmaSerializer, TurmaCreateUpdateSerializer,
    CertificadoSerializer,
)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Alunos.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'cpf', 'matricula']
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'data_de_nascimento', 'matricula']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AlunoCreateUpdateSerializer
        return AlunoSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Cursos.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome_do_curso', 'area_curso']
    search_fields = ['nome_do_curso', 'area_curso']
    ordering_fields = ['nome_do_curso']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CursoCreateUpdateSerializer
        return CursoSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turmas.objects.all()
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome_da_turma', 'data_inicio', 'data_fim']
    search_fields = ['nome_da_turma']
    ordering_fields = ['data_inicio', 'data_fim']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TurmaCreateUpdateSerializer
        return TurmaSerializer


class CertificadoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nome', 'curso']
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'data_emissao']

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nome, curso, data_emissao, email
                FROM certificados_view
            """)
            rows = cursor.fetchall()

        # Formatar dados como dicionário
        certificados = [
            {
                'id': row[0],
                'nome': row[1],
                'curso': row[2],
                'data_emissao': row[3],
                'email': row[4],
            }
            for row in rows
        ]
        return certificados

    def list(self, request, *args, **kwargs):
        certificados = self.get_queryset()
        serializer = CertificadoSerializer(certificados, many=True)
        return Response(serializer.data)
