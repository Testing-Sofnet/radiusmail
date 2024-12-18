from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=150, blank=False)
    group_active = models.BooleanField(default=True)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = 'Grupos'

class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.CharField(max_length=255)
    group = models.ForeignKey(Group, related_name='UsersGroup', on_delete=models.CASCADE)
    expire_date = models.DateField(null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Usuarios'
