from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser
from callboard.models import Ad, Review
from callboard.paginators import AdPagination
from callboard.serializers import AdRetrieveSerializer, AdSerializer, ReviewSerializers
from users.permissions import IsAutor


class AdListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']


class AdRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = AdRetrieveSerializer
    queryset = Ad.objects.all()


class AdCreateAPIView(generics.CreateAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser | IsAutor]
    serializer_class = AdSerializer
    queryset = Ad.objects.all()


class AdDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser | IsAutor]
    queryset = Ad.objects.all()


class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            self.permission_classes = [IsAdminUser | IsAutor]
        return [permission() for permission in self.permission_classes]
