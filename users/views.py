from rest_framework import generics, response, status
from rest_framework.permissions import AllowAny
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import UserRegistrationSerializer, UserRetrieveSerializer, UserPasswordResetSerializer, \
    UserPasswordResetConfirmSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    """Эндпоинт создания пользователя"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Пользователь успешно зарегистрирован!"},
                                 status=status.HTTP_201_CREATED)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Эндпоинт редактирования пользователя"""
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]

    def perform_update(self, serializer):
        user = serializer.save(is_active=True)
        if user.password:
            user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Эндпоинт просмотра пользователя"""
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Эндпоинт удаления пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class UserPasswordResetAPIView(generics.GenericAPIView):
    """Эндпоинт для сброса пароля пользователя"""
    serializer_class = UserPasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Ссылка для сброса пароля отправлена на почту."},
                                 status=status.HTTP_200_OK)


class UserPasswordResetConfirmAPIView(generics.GenericAPIView):
    """Эндпоинт для подтверждения сброса пароля пользователя"""
    serializer_class = UserPasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, **kwargs})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"detail": "Пароль успешно сброшен!"},
                                 status=status.HTTP_200_OK)
