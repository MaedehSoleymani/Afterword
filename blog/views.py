from django.shortcuts import render, redirect, get_object_or_404
from blog.forms import PostForm
from blog.models import Post
from django.contrib import messages
from django.utils import timezone

def home(request):
    posts=Post.objects.order_by('-created_date')
    return render(request,'blog/home.html',{'posts':posts})

def my_posts(request):
    user=request.user
    posts=Post.objects.filter(author=user).order_by('-created_date')
    total_posts=posts.count()
    published_posts=posts.filter(status='published').count()
    draft_posts=posts.filter(status='draft').count()
    scheduled_posts=posts.filter(status='scheduled').count()
    context={'posts':posts,'total_posts':total_posts,'published_posts':published_posts,'draft_posts':draft_posts,'scheduled_posts':scheduled_posts}
    return render(request,'blog/my_posts.html',context)

def write_post(request):
    if request.method=='POST':
        form=PostForm(request.POST)
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
                print(f"{form}")
                messages.success(request,'Your Article was saved successfully.')
                return redirect('blog:my_posts')
            except Exception as e:
                print(f"{e}")
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            print("not valid")
            return redirect('blog:write_post')
    else:
        form=PostForm()
    return render(request,'blog/write_post.html',{'form':form})

def post_actions(request,pid):
    post=get_object_or_404(Post,author=request.user,id=pid)
    if request.method=='POST':
        action=request.POST.get("action")
        if action=="edit":
            return redirect('blog:edit_post',pid=pid)
        elif action=="delete":
            post.delete()
            messages.success(request,'The message has been deleted successfully.')
            return redirect('blog:my_posts')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return redirect('blog:my_posts')
    return redirect('blog:my_posts')
   
def edit_post(request,pid):
    post=get_object_or_404(Post,author=request.user,id=pid)
    if request.method=='POST':
        form=PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            edited_post=form.save(commit=False)
            edited_post.author=request.user
            publish_option=request.POST.get('publish_option')
            if publish_option=='draft':
                edited_post.status=Post.STATUS_DRAFT
                edited_post.publish_date=None
            elif publish_option=='delete':
                edited_post.delete()
                messages.success(request, 'Your post has been deleted successfully.')
                return redirect('blog:my_posts')
            else:
                messages.error(request,'Wrong option. Please choose one in the form.')
            edited_post.save()
            messages.success(request,'Your changes have been applied successfully.')
            return redirect('blog:my_posts')
        else:
            messages.error(request,'The information you entered appears to be invalid. Please check the highlighted fields and correct them.')
            return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
    else:
        form=PostForm(instance=post)
    return render(request,'blog/edit_post.html',{'form':form,'post': post,'now': timezone.now()})

def post_detail(request,pid):
    return render(request,'blog/home.html')