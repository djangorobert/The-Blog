from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostView, Like, Comment
from .forms import PostForm, CommentForm, UserLoginForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
# Create your views here.
class PostListView(ListView):
    model = Post
    queryset = Post.objects.order_by('-publish_date')
    context_object_name = 'post_list'
   

class PostDetailView(DetailView):
    model = Post

    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail", slug=post.slug)
        return redirect("detail", slug=self.get_object().slug)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': CommentForm()
        })
        return context


    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object



class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'create'
        })
        return context
  

class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'update'
        })
        return context
    
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'


def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect('detail', slug=slug)



#The Custom Login and Logout Views
def login_view(request):
    next = request.GET.get('next') #/premium/
    form = UserLoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)
            messages.info(request, 'Succesfully Logged in.')
            if next:
                return redirect(next)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, "posts/login.html", context)

def logout(request):
    return render(request, 'posts/logout.html')

def register_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            auth_user = authenticate(username=user.username, password=password)
            login(request, auth_user)
            messages.info(request, 'Succesfully registered')
            if next:
                return redirect(next)
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'posts/signup.html', context)