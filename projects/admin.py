# from django.contrib import admin
# from .models import Project, Tag


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ["name", "slug", "color"]
#     prepopulated_fields = {"slug": ("name",)}


# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ["title", "featured", "created_at"]
#     list_filter = ["featured", "tags"]
#     search_fields = ["title", "short_description"]
#     prepopulated_fields = {"slug": ("title",)}
#     filter_horizontal = ["tags"]


from django.contrib import admin
from .models import Project, Tag, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3  # Mostra 3 campos vazios para subir imagens de uma vez

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = ('tags',) # Facilita selecionar as tags

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}