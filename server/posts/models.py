import uuid
from django.db import models

from api.models import BaseModel
from users.models import CustomUser

# Create your models here.
class Post(BaseModel):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=700, db_index=True)
    content = models.TextField(max_length=10000)
    article_image=models.CharField(max_length=555, null=True, blank=True)
    slug = models.SlugField(max_length=700, unique=True, db_index=True)
    comment_count = models.IntegerField(null=True, default=0)
    
    def __str__(self) -> str:
        return f"{self.id} | {self.title}"