from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter(name='render_markdown')
def render_markdown(text):
    if not text:
        return ""
    # Converte o markdown para HTML ativando tabelas, blocos de código e quebras de linha
    html = markdown.markdown(
        text,
        extensions=['fenced_code', 'tables', 'nl2br']
    )
    return mark_safe(html)