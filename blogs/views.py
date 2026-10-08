from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Subscriber
from .forms import PostForm, SubscribeForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import escape

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
            messages.success(request, "Post created successfully")
            return redirect("blog_detail", post_id=post.id)
    else:
        form = PostForm()
        messages.error(request, "There was a problem saving post")

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
        form = PostForm(request.POST, request.FILES, instance=post)
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
            try:
                _send_subscriber_welcome_email(email)
            except Exception:
                messages.warning(
                    request,
                    'You are subscribed, but we could not send the confirmation email right now.',
                )
            else:
                messages.success(
                    request,
                    'You are subscribed. A welcome note is on its way to your inbox.',
                )
            return redirect('subscribe')
    return render(request, 'subscribe.html', {'form': form})


def _send_subscriber_welcome_email(email):
    site_name = str(settings.SITE_NAME)
    html_site_name = escape(site_name)
    site_url = str(settings.SITE_URL).rstrip('/')
    html_site_url = escape(site_url)
    subject = f'Welcome to {site_name}'
    text_body = (
        f'Welcome to {site_name}.\n\n'
        'Thank you for subscribing. You will receive occasional stories, '
        'ideas and learning notes from us.\n\n'
            f'Explore the journal: {site_url}/blogs\n\n'
        f'The {site_name} team'
    )
    html_body = f'''<!doctype html>
<html lang="en">
<body style="margin:0;padding:0;background:#fafafa;color:#171717;font-family:Arial,Helvetica,sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#fafafa;padding:36px 12px;">
    <tr><td align="center">
            <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;background:#ffffff;border:1px solid #e5e5e5;">
                <tr><td style="height:5px;background:#c9a227;font-size:0;line-height:0;">&nbsp;</td></tr>
                <tr><td style="padding:32px 42px 22px;border-bottom:1px solid #eeeeee;">
                    <p style="margin:0;color:#171717;font-size:21px;font-weight:bold;letter-spacing:-0.4px;">{html_site_name}</p>
                    <p style="margin:7px 0 0;color:#8d6c17;font-size:11px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;">Practical insights for developers</p>
        </td></tr>
        <tr><td style="padding:34px 42px 42px;">
                    <h1 style="margin:0 0 18px;color:#171717;font-family:Georgia,'Times New Roman',serif;font-size:34px;font-weight:normal;line-height:1.15;">Welcome to {html_site_name}.</h1>
                    <p style="margin:0 0 16px;color:#4b5563;font-size:16px;line-height:1.7;">Thank you for subscribing. You are now on the list.</p>
                    <p style="margin:0 0 26px;color:#4b5563;font-size:16px;line-height:1.7;">We will send occasional practical insights, tutorials, and ideas for developers building modern software.</p>
                    <a href="{html_site_url}/blogs" style="display:inline-block;background:#171717;border-bottom:3px solid #c9a227;color:#ffffff;padding:13px 20px;text-decoration:none;font-size:14px;font-weight:bold;">Explore the latest posts</a>
                    <p style="margin:34px 0 0;color:#6b7280;font-size:14px;line-height:1.6;">Keep building,<br>The {html_site_name} team</p>
        </td></tr>
      </table>
            <p style="margin:18px 0 0;color:#6b7280;font-size:12px;">You received this message because this address was subscribed on {html_site_name}.</p>
    </td></tr>
  </table>
</body>
</html>'''
    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)
    
    
def error_404_view(request, exception):
    return render(request, '404.html', status=404)    
#     post = Post.objects.get(id=post_id)
# except Post.DoesNotExist:
#     raise Http404    