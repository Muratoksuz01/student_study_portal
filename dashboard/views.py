from django.shortcuts import render,redirect
from .forms import NotesForm,HomeworkForm,DashboardForm,TodoForm
from dashboard.models import Notes,Homework,Todo
from django.contrib import messages
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch

# Create your views here.
def home(request):
    return render(request,"dashboard/home.html")
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST["title"],description=request.POST["description"])
            notes.save()
        messages.success(request,f"Notes added from {request.user.username} Succesfully!")
    else:
        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={"notes":notes,"form":form}
    return render(request,"dashboard/notes.html",context)
def delete_note(request,pk):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")    
class notedetailview(DetailView):
    model=Notes


def homework(request):
    if request.method=="POST":
        form=HomeworkForm(request.POST)
        
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                finished=True if finished=="on" else False
            except:
                finished=False
            home=Homework(user=request.user,title=request.POST["title"],description=request.POST["description"],subject=request.POST["subject"],due=request.POST["due"],is_finished=finished)
            home.save()
        messages.success(request,f"Homework added from {request.user.username} Succesfully")
    else:   
        form=HomeworkForm()

    homework=Homework.objects.filter(user=request.user)
    home_done = True if len(homework)==0 else False
    context={
        "homework":homework,
        "home_done":home_done,
        "form":form
        }
    return render(request,"dashboard/homework.html",context)
def update_homework(request,pk):
    homework=Homework.objects.get(id=pk)
    if  homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect("homework")
def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST["text"]
        video=VideosSearch(text,10)
        result_list=[]
        for video in video.result()["result"]:
            result_dict={
                'input':text,
                "title":video["title"],
                "duration":video["duration"],
                "thumbnails":video["thumbnails"][0]["url"],
                "channel":video["channel"]["name"],
                "link":video["link"],
                "views":video["viewCount"]["short"],
                "published":video["publishedTime"],
            }
            
            desc = ""
            if video['descriptionSnippet']:
                for j in video['descriptionSnippet']:
                    desc +=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={"form":form,"results":result_list}
        return render(request,"dashboard/youtube.html",context)
    form=DashboardForm()
    context={"form":form}
    return render(request,"dashboard/youtube.html",context)   

def todo(request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST["is_finished"]
                finished=True if finished=="on" else False
            except:
                finished=False
            todo=Todo(user=request.user,title=request.POST["title"],is_finished=finished)
            todo.save()
        messages.success(request,f"your task added from {request.user} succesfully")
    else:
        form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    todo_done=len(todo)
    context={"form":form,"todos":todo,"todo_done":todo_done}
    return render(request,"dashboard/todo.html",context)
def delete_todo(request,pk):
    todo=Todo.objects.get(id=pk).delete()
    return redirect("todo")

def book(request):
    return render(request,"dashboard/books.html")
