from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	bio = models.TextField(max_length=500, blank=True)
	profile_picture = models.ImageField(
		upload_to='profile_pics/', 
		null=True, 
		blank=True
	)
	followers = models.ManyToManyField(
		'self',
		symmetrical=False,  # If A follows B, B doesn't auto-follow A
		related_name='following',  # Access who someone follows
		blank=True
	)
    
	def __str__(self):
		return self.username
