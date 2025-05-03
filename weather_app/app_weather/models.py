from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the active User model dynamically

class WeatherSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weather_searches", null=True, blank=True)
    city = models.CharField(max_length=100)
    date_searched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} searched by {self.user.username}"
