from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()

@register.inclusion_tag('blog/post/top_display.html')
def post_top():
    top = Post.published.all()[2].title
    return {'top': top}

@register.inclusion_tag('blog/post/detail_body_post.html')
def post_det():
    detail = Post.published.all()[1].body
    return {'detail': detail}

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))