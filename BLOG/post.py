from fastapi.responses import RedirectResponse
import main,schemas,user
from fastapi import APIRouter, Form,HTTPException,status,Depends,Request
from jose import jwt

router = APIRouter(
    tags=['Posts']
)

secret_key= "31e9b624e316ea2ddcb45dd48d2e5fbfcdea135affde7806dcbd48485e1982ac"

@router.post('/post/create')
def createPost(request:Request,title: str = Form(...), 
    content: str = Form(...),):
    f = open('token.txt','r')
    acces_token = f.read()
    result = jwt.decode(acces_token,secret_key)
    user_section = user.getUserSection(result['sub'])
    if user_section != "admin":
        return main.templates.TemplateResponse('error.html',{'request':request})
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have rights")
        
    posts = main.loadPosts()
    lastId = main.getUniqueId(posts)
    newId = lastId + 1
    new_post = {
        'id': newId,
        'title': title,
        'publishingDate': main.current_time(),
        'content': content
    }
    posts.append(new_post)
    main.savePosts(posts)
    # return main.templates.TemplateResponse('add_post.html',{'request':request})
    return main.templates.TemplateResponse('posts.html', {'request': request, 'posts': posts})




@router.get("/posts")
def read_posts(request: Request):
    posts = main.loadPosts()
    return main.templates.TemplateResponse("posts.html", {
        "request": request,
        "posts": posts
    })

@router.get('/post/get')
def getPosts(request:Request):
    raw_posts = main.loadPosts()
    if not raw_posts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='There is no posts yet')
    posts = []
    for post in raw_posts:
        post_info = ({
            'id': post['id'],
            'title': post['title'],
            'publishingDate': post['publishingDate'],
            'content': post['content']
        })
        posts.append(post_info)
    # return main.templates.TemplateResponse('index.html', {'request': request, 'co': posts})
    return post_info
    

@router.get('/post/create')
def get_create_post_page(request: Request):
    return main.templates.TemplateResponse('add_post.html', {'request': request})    


@router.post('/post/update/{id}')
def updatePost(request: Request,id: int, title: str = Form(...), content: str = Form(...)):
    f = open('token.txt', 'r')
    acces_token = f.read()
    result = jwt.decode(acces_token, secret_key)
    user_section = user.getUserSection(result['sub'])
    if user_section != "admin":
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have rights")
        return main.templates.TemplateResponse('error.html',{'request':request})
    posts = main.loadPosts()
    
    for post in posts:
        if post.get('id') == id:
            post['title'] = title
            post['content'] = content
            main.savePosts(posts)
            return main.templates.TemplateResponse('single_post.html', {
                'request': request,
                'post': post
            })

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@router.get('/post/update/{id}')
def update_page(request: Request, id: int):
    posts = main.loadPosts()
    post = None
    for p in posts:
        if p.get('id') == id:
            post = p
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return main.templates.TemplateResponse('update_post.html', {
        'request': request,
        'post': post
    })
    
@router.get('/post/get/{id}')
def getPostById(id:int,request:Request):
    posts = main.loadPosts() 
    for post in posts: 
        if post.get('id') == id:
            postInfo = {
                'id': post['id'],
                'title': post['title'],
                'publishingDate': post['publishingDate'],
                'content': post['content']
            }
            return main.templates.TemplateResponse("single_post.html", {
                "request": request,
                "post": postInfo
            })


@router.post('/post/delete/{id}')
def deletePost(id: int, request: Request): 
    f = open('token.txt', 'r')
    acces_token = f.read()
    result = jwt.decode(acces_token, secret_key)
    user_section = user.getUserSection(result['sub'])
    if user_section != "admin":
        return main.templates.TemplateResponse('error.html',{'request':request})
        # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You dont have rights")
    
    posts = main.loadPosts()
    for post in posts:
        if post.get('id') == id:
            posts.remove(post)
            main.savePosts(posts)
    return main.templates.TemplateResponse("posts.html", {
        "request": request,
        "posts": posts
    })
            
    

    

    
    


