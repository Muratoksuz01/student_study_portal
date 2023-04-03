from django.shortcuts import render,redirect
from .forms import NotesForm,HomeworkForm,DashboardForm,TodoForm,ConvarsionForm,ConversionLengthForm,ConversionMassForm,UserRegisterForm
from dashboard.models import Notes,Homework,Todo
from django.contrib import messages
from django.views.generic.detail import DetailView
from youtubesearchpython import VideosSearch
import requests,wikipedia
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
def update_todo(request,pk):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect("todo")

def book(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST["text"]
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]

        for i in range(10):
            result_dict={
                "title":answer["items"][i]["volumeInfo"]["title"],
                'subtitle': answer ['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer ['items'][i]['volumeInfo'].get('description'),
                'count': answer ['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer ['items'][i]['volumeInfo'].get('categories'),
                'rating': answer ['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get("thumbnail"),
                'preview':( answer ['items'][i]['volumeInfo'].get('previewLink'))
                
            }
            
            
            result_list.append(result_dict)
            context={"form":form,"results":result_list}
        return render(request,"dashboard/books.html",context)
    form=DashboardForm()
    context={"form":form}
    return render(request,"dashboard/books.html",context) 

def dictionary(request):
    if request.method=="POST":
        form = DashboardForm(request. POST)
        text = request. POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        r = requests.get(url)
        answer = r.json ()
        # print(json.dumps(answer,indent=0))
        # print(answer [0]['phonetics'][0]['text'])
        # print(answer [0]['phonetics'][0]['audio'])
        # print(answer [0]['meanings'][0]['definitions'][0]['definition'])
        # print(answer [0] ['meanings'][0]['definitions'][0]['example'])
        # print(answer [0] ['meanings'][0]['definitions'][0]['synonyms'])


        
        phonetics = answer [0]['phonetics'][0]['text']
        audio = answer [0]['phonetics'][0]['audio']
        definition = answer [0]['meanings'][0]['definitions'][0]['definition']
       # example = answer [0] ['meanings'][0]['definitions'][0]['example']
        synonyms = answer [0] ['meanings'][0]['definitions'][0]['synonyms']
        context = {
        'form': form,
        'input': text,
        'phonetics': phonetics,
        'audio': audio,
        'definition': definition,
       # "example":example,
        "synonyms":synonyms
        }
        
            # context = {
            #     "form":form,
            #     "input":""
            # }

        return render (request, "dashboard/dictionary.html", context)


    form = DashboardForm()
    context = {'form' : form}
    return render (request, "dashboard/dictionary.html", context)

def wiki(request):
    if request.method=="POST":
        text=request.POST["text"]
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            "form":form,
            "title":search.title,
            "link":search.links,
            "details":search.summary
        }
        return render(request, "dashboard/wiki.html",context)


    form=DashboardForm()
    context = {
        'form': form}
    return render(request, "dashboard/wiki.html",context)

def conversion(request):
    if request.method=="POST":
        form=ConvarsionForm(request.POST)
        if request.POST["measurement"]=="length":
            measurement_form=ConversionLengthForm()
            context={"form":form,"m_form":measurement_form,"input":True}
            if "input" in request.POST:
                first=request.POST["measure1"]
                second=request.POST["measure2"]
                input=request.POST["input"]
                answer=""
                if input and int(input)>=0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input)*3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input)/3} yard'
                context = {
                    'form' : form,
                    'm_form' :measurement_form,
                    'input': True,
                    'answer': answer
                    }
        else:
            if request.method=="POST":
                form=ConvarsionForm(request.POST)
                if request.POST["measurement"]=="mass":
                    measurement_form=ConversionMassForm()
                    context={"form":form,"m_form":measurement_form,"input":True}
                    if "input" in request.POST:
                        first=request.POST["measure1"]
                        second=request.POST["measure2"]
                        input=request.POST["input"]
                        answer=""
                        if input and int(input)>=0:
                            if first == 'pound' and second == 'kilogram':
                                answer = f'{input} pound = {int(input)*0.453592} kilogram'
                            if first == 'kilogram' and second == 'pound':
                                answer = f'{input} foot = {int(input)/2.20462} yard'
                        context = {
                            'form' : form,
                            'm_form' :measurement_form,
                            'input': True,
                            'answer': answer
                            }
    else:
        form=ConvarsionForm()
        context={
            "form":form,
            "input":False
        }
    return render(request,"dashboard/conversion.html",context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm (request. POST)
        if form.is_valid ():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success (request, f"Account Created for {username}")
            return redirect("login")
    else:
        form=UserRegisterForm()
    context={"form":form}
    return render(request,"dashboard/register.html",context)

def profile(request):
    todo=Todo.objects.filter(is_finished=False, user=request.user)
    homework=Homework.objects.filter(is_finished=False,user=request.user)
    context={"todos":todo,"homeworks":homework}
    return render(request,"dashboard/profile.html",context)




