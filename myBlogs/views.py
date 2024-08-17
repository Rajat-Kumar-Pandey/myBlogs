from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, Category
from .forms import CreateBlogForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404

# Create your views here.

# def index(request):
#     keyword = request.GET.get("search")
#     msg=None
#     paginator = None
#     if keyword:
#         blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | 
#                                     Q(category__title__icontains=keyword))
        
#         if blogs.exists():
#             pass
#             # paginator = Paginator(blogs, 4)
#             # blogs = paginator.page(1)
        
#         else:
#             msg = "There is no article with the keyword"
            
#     else:
#         blogs = Blog.objects.filter(featured=False)
#         paginator = Paginator(blogs, 4)
#         page = request.GET.get("page")
        
#         try:
#             blogs = paginator.page(page)
            
#         except PageNotAnInteger:
#             blogs = paginator.page(1)
        
#         except EmptyPage:
#             blogs = paginator.page(paginator.num_pages)

    
    
#     f_blog = Blog.objects.filter(featured=True).first() if not keyword else blogs.object_list.first()
        
#     categories = Category.objects.all()
#     context = {"blogs":blogs, "f_blog":f_blog, "msg":msg, "paginator": paginator, "cats": categories}
#     return render(request, "myBlogs/index.html", context)

def index(request):
    keyword = request.GET.get("search")
    msg = None
    paginator = None

    if keyword:
        # Filter blogs based on the search keyword
        blogs = Blog.objects.filter(
            Q(title__icontains=keyword) | 
            Q(body__icontains=keyword) | 
            Q(category__title__icontains=keyword)
        )

        if not blogs.exists():
            msg = "There is no article with the keyword"
            f_blog =None
        
        # Paginate the search results
        paginator = Paginator(blogs, 4)
        page = request.GET.get("page", 1)
        
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
    
    else:
        # Retrieve non-featured blogs for default view
        blogs = Blog.objects.filter(featured=False)
        paginator = Paginator(blogs, 4)
        page = request.GET.get("page", 1)
        
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

    # Fetch the featured blog if no search keyword is provided
    f_blog = Blog.objects.filter(featured=True).first() 

    # Get all categories
    categories = Category.objects.all()

    # Context to pass to the template
    context = {
        "blogs": blogs,
        "f_blog": f_blog,
        "msg": msg,
        "paginator": paginator,
        "cats": categories
    }

    return render(request, "myBlogs/index.html", context)


def detail(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise Http404("Blog not found")

    related_blogs = Blog.objects.filter(category__id=blog.category.id).exclude(id=blog.id)[:4]
    comments = Comment.objects.filter(blog=blog)
    form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user 
                comment.save()
                return redirect("detail", slug=blog.slug)

    context = {'blog': blog, "form": form, "comments": comments, "r_blogs": related_blogs}
    return render(request, "myBlogs/detail.html", context)

@login_required(login_url="signin")
def create_article(request):
    form=CreateBlogForm()
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(request.POST["title"])
            blog.user=request.user
            blog.save()
            messages.success(request, "Article created successfully!")
            return redirect("profile")
    context = {"form": form}
    return render(request, "myBlogs/create.html", context)
    
    
# @login_required(login_url="signin")
# def update_article(request, slug):
#     update = True
#     blog = Blog.objects.get(slug=slug)
#     form=CreateBlogForm(instance=blog)
#     if request.method == 'POST':
#         form = CreateBlogForm(request.POST, request.FILES, instance=blog)
#         blog = form.save(commit=False)
#         blog.slug=slugify(request.POST["title"])
#         blog.save()
#         messages.success(request, "Article updated successfully")
#         return redirect("profile")
#     context={"update":update, "form":form}
#     return render(request, "myBlogs/create.html", context)
@login_required(login_url="signin")
def update_article(request, slug):
    # Fetch the blog instance or return a 404 if not found
    blog = get_object_or_404(Blog, slug=slug)
    form = CreateBlogForm(instance=blog)
    
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            blog = form.save(commit=False)
            # Update the slug based on the new title
            blog.slug = slugify(form.cleaned_data["title"])
            # Save the blog instance
            blog.save()
            messages.success(request, "Article updated successfully")
            return redirect("profile")
        else:
            # Add form errors to messages
            messages.error(request, "There was an error updating the article. Please check the form and try again.")
    
    context = {"update": True, "form": form}
    return render(request, "myBlogs/create.html", context)


@login_required(login_url="signin")
def delete_article(request, slug):
    blog = Blog.objects.get(slug=slug)
    blogs = Blog.objects.filter(user=request.user)
    delete_article = True
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Article deleted successfully")
        return redirect("profile")
    context = {"blog": blog, "del":delete_article, "blogs": blogs}
    return render(request, "myDude/profile.html", context)
    