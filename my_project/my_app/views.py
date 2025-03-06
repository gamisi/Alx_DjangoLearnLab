from django.shortcuts import render
from rest_framework import generics, viewsets, filters
from django_filters import rest_framework as django_filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination  

# Create your views here.
class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    published_after = django_filters.DateFilter(field_name='published_date', lookup_expr='gte')
    published_before = django_filters.DateFilter(field_name='published_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'published_after', 'published_before']

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related('author')  # Optimize with select_related for ForeignKey
    serializer_class = BookSerializer
    filter_backends = (filters.OrderingFilter, django_filters.DjangoFilterBackend)
    filterset_class = BookFilter  # Use custom filter class
    ordering_fields = ['published_date', 'title']
    ordering = ['published_date']  # Default ordering by published date
    permission_classes = [IsAuthenticated]  # Optionally enforce authentication

    # Optional: Use pagination for large datasets
    pagination_class = CustomPagination

    # Customizing the queryset to handle any dynamic filtering or related optimizations
    def get_queryset(self):
        queryset = super().get_queryset()

        # Example of additional dynamic filtering
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        return queryset
    