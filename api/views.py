from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate , login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes 
from .serializers import RegisterSerializer, UserSerializer, NoteSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.shortcuts import get_object_or_404
from .models import NotesLoan

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializers = RegisterSerializer(data = request.data)
    serializers.is_valid(raise_exception=True)
    
    serializers.save()
    
    return Response({ "user": "register successuful"}, status=status.HTTP_201_CREATED,)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if not username or not password:
        return Response({'error':'please write correct username or password'}, status=status.HTTP_400_BAD_REQUEST) 
    
    user = authenticate(request,username=username,password=password,)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response({'refresh': str(refresh),'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid username or password"},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_view(request):
    serializer = TokenRefreshSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message':'Logout successuful'}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def create_noteloan_view(request):
    if request.method == 'GET':
        transactions = NotesLoan.objects.filter(user=request.user)
        transaction_type = request.query_params.get('type')
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)
            
        serializer = NoteSerializer(transactions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def deteil_update_view(request, id):
    
    transaction = get_object_or_404(NotesLoan,id=id,user=request.user)
    if request.method == 'GET':
        serializer = NoteSerializer(transaction)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = NoteSerializer( transaction, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    