from django.urls import path
from .import views

urlpatterns = [
    path("", views.notes, name="notes"),
    path("notes/<slug:slug>/" , views.note_detail,name="note-detail"),
    path("notes-search/", views.search_notes, name='notes-search')
]

# http://127.0.0.1:8000/myNotepad/note
# http://127.0.0.1:8000/myNotepad/note-slug