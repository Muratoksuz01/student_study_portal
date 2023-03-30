from django import forms
from . import models

class NotesForm(forms.ModelForm):
    class Meta:
        model=models.Notes
        fields=["title","description"]

class DateInput(forms.DateInput):
    input_type="date"
class HomeworkForm(forms.ModelForm):
    class Meta:
        model=models.Homework
        widgets={"due":DateInput}
        fields=["subject","title","description","due","is_finished"]

class DashboardForm(forms.Form):
    text=forms.CharField(max_length=200,label="Enter Youtube Search:")

class TodoForm(forms.ModelForm):
    class Meta:
        model=models.Todo
        fields=["title","is_finished"]