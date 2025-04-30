from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    context = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        base_slug = slug
        count = 1
        while Article.objects.filter(slug=slug).exists():
            base_slug = slug + str(count)
            count += 1

        self.slug = base_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

