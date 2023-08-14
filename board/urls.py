from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    # 글목록
    path('postlist/', views.postlist, name='postlist'),
     
    # 글 페이지
    path('post/<int:post_no>/', views.post, name='post'),
    
    
    # 글 crud
   
    path('post/write/', views.write, name='write'),
    path('post/post/', views.post, name='post'),
    path('post/<int:post_no>/update/',views.update, name="post_update"),
    path('post/<int:post_no>/delete/',views.delete, name="post_delete"),
    # path('post/<int:post_no>/download/',views.download, name="post_file_download"),
    
    # 댓글
    path('post/<int:post_no>/comment_write/',views.comment_write, name="comment_write"),
    # path('post/<int:post_no>/comment_delete/<int:comment_no>',views.comment_delete, name="comment_delete"),
    
]