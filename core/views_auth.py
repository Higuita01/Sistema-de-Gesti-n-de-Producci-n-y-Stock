from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# 🔍 ESTADO DEL SISTEMA
@method_decorator(csrf_exempt, name='dispatch')
class EstadoSistemaView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({
            "usuario_existe": User.objects.count() > 0
        })


# 🧑‍💻 REGISTRO ÚNICO (SOLO 1 USUARIO)
@method_decorator(csrf_exempt, name='dispatch')
class RegistroUnicoView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        if User.objects.count() >= 1:
            return Response(
                {"error": "Ya existe un usuario creado"},
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username y password son requeridos"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return Response({"mensaje": "Usuario creado correctamente"})


# 🔐 LOGIN
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Credenciales incorrectas"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response({"mensaje": "Login correcto"})