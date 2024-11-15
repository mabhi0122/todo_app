from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    # def update_title(self, new_title):
    #     self.title = new_title
    #     self.created_at = timezone.now()
    #     self.save()

    def __str__(self):
        return f'{str(self.pk)} - {self.title}'
