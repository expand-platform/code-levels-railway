from django.views import View
from django.shortcuts import render, get_object_or_404
from platform_web.models.blog.BlogPost import BlogPost


class BlogView(View):
    template_name = "website/dashboard/pages/blog.html"

    def get(self, request):
        # Get last 10 published blog posts
        blog_posts = BlogPost.objects.filter(is_published=True).order_by("-published_at")[:10]
        return render(request, self.template_name, {"blog_posts": blog_posts})


class BlogDetailView(View):
    template_name = "website/dashboard/pages/blog_details.html"

    def get(self, request, slug):
        blog_post = get_object_or_404(BlogPost, slug=slug, is_published=True)
        return render(request, self.template_name, {"blog_post": blog_post})
