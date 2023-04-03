from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name="home"),
    path("notes",views.notes,name="notes"),
    path("delete_notes/<int:pk>",views.delete_note,name="delete"),
    path("note-detail/<int:pk>",views.notedetailview.as_view(),name="detail"),
    

    path("update/<int:pk>",views.update_homework,name="update"),
    path("homework",views.homework,name="homework"),
    path("delete_homework/<int:pk>",views.delete_homework,name="delete_homework"),

    path("youtube/",views.youtube,name="youtube"),

    path("todo/",views.todo,name="todo"),
    path("delete_todo/<int:pk>",views.delete_todo,name="delete_todo"),
    path("update_todo/<int:pk>",views.update_todo,name="update_todo"),

    path("book/",views.book,name="book"),
    
    path("dictionary/",views.dictionary,name="dictionary"),
    

    path("wiki/",views.wiki,name="wiki"),

    path("conversion/",views.conversion,name="conversion"),




]
