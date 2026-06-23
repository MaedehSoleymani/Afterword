from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm
from blog.models import Post
from django.contrib import messages
from django.utils import timezone
from django.db.models import F
from accounts.decorators import c_login_required, author_required, admin_required

def home(request):
    filter_type = request.GET.get('filter', 'all')
    search_query = request.GET.get('q', '')    
    posts = Post.objects.filter(status='published', publish_date__lte=timezone.now()).order_by('-created_date')
    if filter_type == 'recent':
        posts = posts.order_by('-publish_date')
    elif filter_type == 'popular':
        posts = posts.order_by('-created_date')
    
    if search_query:
        posts = posts.filter(
            models.Q(title__icontains=search_query) |
            models.Q(content__icontains=search_query)
        )
    
    from django.core.paginator import Paginator
    paginator=Paginator(posts, 9)
    page_number=request.GET.get('page')
    posts_page=paginator.get_page(page_number)
    total_posts=Post.objects.filter(status='published', publish_date__lte=timezone.now()).count()
    total_authors=Post.objects.values('author').distinct().count()
    this_month_posts=Post.objects.filter(
        status='published',
        publish_date__lte=timezone.now(),
        created_date__month=timezone.now().month).count()
    
    context = {
        'posts': posts_page,
        'total_posts': total_posts,
        'total_authors': total_authors,
        'this_month_posts': this_month_posts,
        'now': timezone.now()
    }
    return render(request, 'blog/user_blog.html', context)

def post_detail(request, pid):
    post=get_object_or_404(Post, id=pid, status='published', publish_date__lte=timezone.now())
    post.increment_views()
    related_posts=Post.objects.filter(
        author=post.author, 
        status='published', 
        publish_date__lte=timezone.now()
    ).exclude(id=post.id).order_by('-created_date')[:3]
    author_post_count = Post.objects.filter(
        author=post.author, 
        status='published', 
        publish_date__lte=timezone.now()).count()
    context={'post': post,'related_posts': related_posts,'author_post_count': author_post_count}
    return render(request, 'blog/post_detail.html', context)

@c_login_required
@author_required
def author_dashboard(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_date')
    total_posts = posts.count()
    published_posts = posts.filter(status='published').count()
    draft_posts = posts.filter(status='draft').count()
    scheduled_posts = posts.filter(status='scheduled').count()
    context = {
        'posts': posts,
        'total_posts': total_posts,
        'published_posts': published_posts,
        'draft_posts': draft_posts,
        'scheduled_posts': scheduled_posts
    }
    return render(request, 'blog/author_dashboard.html', context)

@c_login_required
@author_required
def write_post(request):
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES)

        print("FILES in request:", request.FILES)
        print("img in request.FILES:", 'img' in request.FILES)
        if 'img' in request.FILES:
            print("File name:", request.FILES['img'].name)

        if form.is_valid():
            print("valid form")
            post=form.save(commit=False)
            post.author=request.user
            publish_option=request.POST.get('publish_option')
            if publish_option=='draft':
                post.status=Post.STATUS_DRAFT
                post.publish_date=None
            elif publish_option=='now':
                post.status=Post.STATUS_PUBLISHED
                post.publish_date=timezone.now()
            elif publish_option=='schedule':
                post.status=Post.STATUS_SCHEDULED
            else:
                messages.error(request,'Wrong option. Please choose one in the form.')
            try:
                post.save()

                print(f"Post saved! Image: {post.img}")
                print(f"Image URL: {post.img.url if post.img else 'No image'}")
                print(f"{form}")

                messages.success(request,'Your Article was saved successfully.')
                return redirect('blog:author_dashboard')
            except Exception as e:
                print(f"{e}")
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            print("Form errors:", form.errors)
            return redirect('blog:write_post')
    else:
        form=PostForm()
    return render(request,'blog/author_write_post.html',{'form':form})

@c_login_required
@author_required
def post_actions(request,pid):
    post=get_object_or_404(Post,author=request.user,id=pid)
    if request.method=='POST':
        action=request.POST.get("action")
        if action=="edit":
            return redirect('blog:edit_post',pid=pid)
        elif action=="delete":
            post.delete()
            messages.success(request,'The message has been deleted successfully.')
            return redirect('blog:author_dashboard')
        elif action=="publish":
            post.status=Post.STATUS_PUBLISHED
            post.save(update_fields=['status'])
            messages.success(request,"Post published successfully.")
            return redirect('blog:author_dashboard')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return redirect('blog:author_dashboard')
    return redirect('blog:author_dashboard')

@c_login_required
@author_required
def edit_post(request, pid):
    post=get_object_or_404(Post, author=request.user, id=pid)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post=form.save(commit=False)
            edited_post.author = request.user
            publish_option = form.cleaned_data('publish_option')
            
            if publish_option == 'draft':
                edited_post.status = Post.STATUS_DRAFT
                edited_post.publish_date = None
            elif publish_option == 'now':
                edited_post.status = Post.STATUS_PUBLISHED
                edited_post.publish_date = timezone.now()
            elif publish_option == 'schedule':
                edited_post.status = Post.STATUS_SCHEDULED
            elif publish_option == 'delete':
                post.delete()
                messages.success(request, 'Your post has been deleted successfully.')
                return redirect('blog:author_dashboard')
            else:
                pass
            
            edited_post.save()
            messages.success(request, 'Your changes have been applied successfully.')
            return redirect('blog:author_dashboard')
        else:
            messages.error(request, 'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return render(request, 'blog/author_edit_post.html', {'form': form, 'post': post})
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/author_edit_post.html', {'form': form, 'post': post, 'now': timezone.now()})
