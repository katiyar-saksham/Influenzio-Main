from django.db import models
from django.contrib.auth.models import User
from app.managers import ThreadManager

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        abstract = True

class Thread(BaseModel):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group','Group')
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices = THREAD_TYPE, default='group')
    users = models.ManyToManyField('auth.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.thread_type == 'personal' and self.users.count() == 2:
            return f'{self.users.first()} and {self.users.last()}'
        return f'{self.name}'

class Message(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='get_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self):
        return f'message {self.id} from {self.sender} in thread <{self.thread}>'