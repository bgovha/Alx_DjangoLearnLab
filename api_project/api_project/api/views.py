from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_overview(request):
    return Response({
        'message': 'Welcome to the Book API!',
        'endpoints': {
            'books': '/api/books/ (coming soon)',
        }
    })
# Create your views here.
