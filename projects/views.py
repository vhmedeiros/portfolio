from django.shortcuts import render, get_object_or_404
from .models import Project, Tag


def project_list(request):
    tag_slug = request.GET.get("tag", "")
    projects = Project.objects.prefetch_related("tags").all()
    tags = Tag.objects.all()

    if tag_slug:
        projects = projects.filter(tags__slug=tag_slug)

    # HTMX: retorna só o fragmento da lista
    if request.htmx:
        return render(request, "projects/partials/project_grid.html", {
            "projects": projects,
            "active_tag": tag_slug,
        })

    return render(request, "projects/project_list.html", {
        "projects": projects,
        "tags": tags,
        "active_tag": tag_slug,
    })


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, "projects/project_detail.html", {"project": project})
