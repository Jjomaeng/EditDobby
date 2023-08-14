import datetime
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Post, Member, Comment, Postfile

# Create your views here.
def postlist(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")

    page = request.GET.get('page', '1')
    search_keyword = request.GET.get('keyword', '')
    search_type = request.GET.get('type', '')
    post_list = Post.objects.all()
    
    if search_type == 'all':
        post_list = post_list.filter(Q(post_title__icontains=search_keyword) |
                                    Q(post_detail__icontains=search_keyword) |
                                    Q(member_id__member_id__icontains=search_keyword)
                                    )
    elif search_type == 'post_title':
        post_list = post_list.filter(post_title__icontains=search_keyword)    
    elif search_type == 'post_detail':
        post_list = post_list.filter(post_detail__icontains=search_keyword)    
    elif search_type == 'member_id':
        post_list = post_list.filter(member_id__member_id__icontains=search_keyword)
    
    paginator = Paginator(post_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    print(page_obj)

    count = len(post_list)
    context = {'post_list': page_obj, 'page': page, 'keyword': search_keyword , 'count':count}
    
    return render(request, 'board/postlist.html', context)

def post(request, post_no):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    if request.method == 'GET':
        post = Post.objects.get(post_no=post_no)
        comments = Comment.objects.filter(post_no=post_no)

        try:
            postfile = Postfile.objects.get(post_no=post_no)
            context = {
                'post':post,
                'comments':comments,
                'postfile':postfile,
            }
        except Postfile.DoesNotExist:
            context = {
                'post':post,
                'comments':comments,
            }        

        return render(request, 'board/post.html', context)
    
    
    # post메서드(댓글등록,삭제)
    else:
        comment = Comment()
        comment.post = post_no
        comment.body = request.POST['body']
        comment.date = datetime.now()
        comment.save()
        return render(request, 'board/post.html', 
                      {'post':post})


##########################################################
# def download(request, post_no):
#     if request.method == 'POST':
#         fn = request.POST["filename"]
#         filename = Postfile.objects.filter(post_no = post_no)
#         filepath = str(settings.BASE_DIR) + ('/media/%s' % filename.file_name)
#         fn = urllib3.parse.quote(fn.encode('utf-8'))
#         with open(filepath, 'rb') as f:
#             response = HttpResponse(f, content_type='application/octet-stream')
#             response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % fn
                
#     return redirect('/board/post/'+post_no)
############################################################


def write(request):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    
    if request.method == 'POST':
        save_post_title = request.POST.get('postname')
        save_post_detail = request.POST.get('contents')
        s_id = request.session.get('s_id')
        save_member_id = Member.objects.get(member_id=s_id)
    
        now = datetime.datetime.now()
        
        a = Post(
            post_title = save_post_title,
            post_detail = save_post_detail,
            post_update = now,
            member_id = save_member_id,
        )
        a.save()
        
        
        # 파일 저장 ----- 작업중
        # try:
        #     upload_file = request.FILES.get('up_file')
            
            
        #     # 파일이 있으면 파일저장
        #     file = Postfile(
        #             postfile_name = upload_file.name,
        #             postfile_root = "\\static\\postfiles\\" + upload_file.name,
        #             member_id = save_member_id
        #         )
        #     file.save()

        #     try:
        #         with open(STATIC_ROOT+'\\postfiles\\'+upload_file.name, 'wb') as file: 
        #             for chunk in upload_file.chunks():
        #                 file.write(chunk)
        #     except FileNotFoundError:
        #         file.delete()
            
        #     # 파일이 없으면 글 작성/수정
        # except upload_file.:
        #     return redirect('/board/postlist/')



            
        # 글이 써지면 목록으로
        return redirect('/board/postlist/')
        
    else:
        # get 메서드    
        
        return render(request, 'board/write.html')
    

def update(request, post_no):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    post = Post.objects.get(post_no=post_no)
    #
    # postfile = Postfile.objects.filter(post_no = post_no)
    #
    if request.method == "POST":
        post.post_title = request.POST['postname']
        post.post_detail = request.POST['contents']
        # post.post_update = datetime.now()
        try:
            post.file = request.FILES['image']
        except:
            post.file = None
        post.save()
        return redirect('/board/post/'+str(post.post_no),{'post':post})
    else:
        post=Post.objects.get(post_no = post_no)
        return render(request, 'board/write.html', {'post':post})




def delete(request, post_no):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    post = Post.objects.get(post_no=post_no)
    post.delete()
    return redirect("/board/postlist/")







def comment_write(request, post_no):
    s_id = request.session.get('s_id') # session id 유무 체크
    if s_id==None:
        return redirect("/main/login/")
    
    if request.method == 'POST':
        now = datetime.datetime.now()
        s_id = request.session.get('s_id')
        jsonObject = json.loads(request.body)
        # t_post_no = jsonObject.get('post_no')
        reply = Comment.objects.create(
            # 
            post_no=Post.objects.get(post_no=post_no),
            member_id=Member.objects.get(member_id=s_id),
            comment_detail=jsonObject.get('comment_detail'),
            comment_update = now
        )
        reply.save()
        
        membername = Member.objects.get(member_id = s_id)
        context = {
            # 'name': serializers.serialize("json", reply.member_no),
            'content': reply.comment_detail,
            'pp': membername.member_nick    
        }

        return JsonResponse(context)


# def comment_delete(request):
#     comment = Comment.objects.get(comment_no=comment_no)
#     post.delete()
#     return


def file():
    
    return 