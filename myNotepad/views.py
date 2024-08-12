from django.shortcuts import render
from myNotepad.models import Note
from myNotepad.serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

# Create your views here.



@api_view(['GET'])
def search_notes(request):
    query = request.query_params.get("search", "")
    
    # Handle empty query case
    if not query:
        return Response({"detail": "Search query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Perform the search
    notes = Note.objects.filter(
        Q(title__icontains=query) | 
        Q(body__icontains=query) | 
        Q(category__icontains=query)
    )
    
    # Serialize and return the results
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET", "POST"])
def notes(request):
    if request.method == "GET":
        notes = Note.objects.all()
        serializer = NoteSerializer(notes,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def note_detail(request, slug):
    try:
        note = Note.objects.get(slug=slug)
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET' , 'PUT' , 'DELETE'])
# def note_detail(request,slug):
#     try:
#         note = Note.objects.get(slug=slug)
#     except Note.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#     elif request.method =='PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)