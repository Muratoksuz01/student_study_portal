from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    
    class Meta:
        verbose_name="notes"#kullanıcı okuyucu tarafından kullanıcıboyle görecek 
        verbose_name_plural="notes"#verbose_name_plural özelliği, model sınıfının adının sonuna “s” ekleyerek varsayılan olarak ayarlanır

    def __str__(self):
        return self.title
    


class Homework(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subject=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_finished=models.BooleanField(default=False)
    class Meta:
        verbose_name="todo"#kullanıcı okuyucu tarafından kullanıcıboyle görecek 
        verbose_name_plural="todo"#verbose_name_plural özelliği, model sınıfının adının sonuna “s” ekleyerek varsayılan olarak ayarlanır

    def __str__(self):
        return self.title