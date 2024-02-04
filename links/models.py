from django.db import models

# Create your models here.
class Link(models.Model):
    original = models.URLField(max_length=800)
    short = models.CharField(max_length=30, primary_key = True)
    clicks = models.IntegerField(default=0)

    def click(self):
        self.clicks += 1
        self.save()
        return self.original

    def __str__(self):
        return self.original

class Click(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    def __str__(self):
        return self.date