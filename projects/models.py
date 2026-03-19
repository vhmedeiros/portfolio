from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default="#6366f1", help_text="Hex color, ex: #6366f1")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    short_description = models.CharField(max_length=300)
    full_description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="projects", blank=True)
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True, help_text="Link para demo ou repositório")
    repo_url = models.URLField(blank=True, null=True, help_text="Link do GitHub")
    featured = models.BooleanField(default=False, help_text="Exibir na página inicial")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
