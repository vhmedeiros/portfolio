from django.contrib import admin
from .models import Project, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "color"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "featured", "created_at"]
    list_filter = ["featured", "tags"]
    search_fields = ["title", "short_description"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
