from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Subscriber
from .forms import PostForm, SubscribeForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages

# Create your views here.
def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def home(request):
    posts = Post.objects.all().order_by("-id")

    return render(
        request,
        "index.html",
        {"posts": posts}
    )

def blogs(request):
    posts = Post.objects.all()# SELECT * FROM posts
    return render(request, 'blogs.html', {"posts": posts})

def blog_detail(request, post_id):
    # post = Post.objects.get(id=post_id)
    post = get_object_or_404(Post, id=post_id)
    return render(request, "blog_detail.html", {"post": post})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # Assign the currently logged-in user.
            post.user = request.user
            post.save()
            return redirect("blog_detail", post_id=post.id)
    else:
        form = PostForm()

    return render(
        request,
        "post_form.html",
        {
            "form": form,
            "page_title": "Create Post",
            "button_text": "Publish Post",
        },
    )


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Only the author can edit the post.
    if post.user != request.user:
        return redirect("blog_detail", post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "post_form.html",
        {
            "form": form,
            "page_title": "Edit Post",
            "button_text": "Update Post",
            "post": post,
        },
    )

@require_http_methods(['GET', 'POST'])
def subscribe(request):
    form = SubscribeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email'].strip().lower()
        if Subscriber.objects.filter(email=email).exists():
            messages.info(request, 'You are already subscribed.')
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, 'Thanks for subscribing. You are on the list!')
            return redirect('subscribe')
    return render(request, 'subscribe.html', {'form': form})
#     post = Post.objects.get(id=post_id)
# except Post.DoesNotExist:
#     raise Http404    