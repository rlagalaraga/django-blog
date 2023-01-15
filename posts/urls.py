from django.urls import path
from posts.views import DashboardView, AddBlogPost, UpdateBlogPost, PostDetailView, delete_Post, LikeView

app_name= 'posts'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('<int:id>/', PostDetailView.as_view(), name='postDetail'),
    path('<int:id>/update_post', UpdateBlogPost.as_view(), name='postEdit'),
    path('<int:id>/delete_post', delete_Post, name='postDelete'),
    path('<int:id>/like', LikeView, name='like_post'),
    path('add-blog/', AddBlogPost.as_view(), name='add-blog'),
]