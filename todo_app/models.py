from django.db import models


class ToDo(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=2000)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

# root
    # root
