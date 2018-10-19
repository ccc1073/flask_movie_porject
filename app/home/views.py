from . import home
from flask import render_template,redirect,url_for,session,request,flash
from functools import wraps
from app import db,app
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import uuid,os,datetime
from app.models import User,Userlog,Preview,Tag,Moviecol,Movie,Comment
from .forms import LoginForm,RegistForm,UserdetailForm,PwdForm,CommentForm


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 会员登录装饰器
def user_login_req(func):
    @wraps(func)
    def decorated_function(*args,**kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login',next=request.url))
        return func(*args,**kwargs)
    return decorated_function


# 会员登录
@home.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(
            name=data['name']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for('home.login'))
        session['user'] = user.name
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip = request.remote_addr
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for('home.index',page=1))

    return render_template('home/login.html',form=form)


# 会员退出
@home.route('/logout/')
def logout():
    session.pop('user',None)
    session.pop('user_id',None)
    return redirect(url_for('home.login'))


# 会员注册
@home.route('/regist/',methods=['GET','POST'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name = data['name'],
            email = data['email'],
            phone = data['phone'],
            pwd = generate_password_hash(data['pwd']),
            uuid = uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功','ok')

    return render_template('home/regist.html',form=form)

# 会员中心以及资料修改
@home.route('/user/',methods = ['GET','POST'])
# @user_login_req
def user():
    # form = UserdetailForm()
    # user_s = User.query.get(int(session['user_id']))
    # form.face.validators = []
    # if request.method == 'GET':
    #     form.name.data = user_s.name
    #     form.email.data = user_s.email
    #     form.phone.data = user_s.phone
    #     form.info.data = user_s.info
    # if form.validate_on_submit():
    #     data = form.data
    #     file_face = secure_filename(form.face.data.filename)
    #     if not os.path.exists(app.config['FC_DIR']):
    #         os.makedirs(app.config['FC_DIR'])
    #         os.chmod(app.config['FC_DIR'], 'rw')
    #         user_s.face = change_filename(file_face)
    #     form.face.data.save(app.config['FC_DIR']+user_s.face)
    #
    #     email_count = User.query.filter_by(email=data['email']).count()
    #     if data['email'] != user_s.email and email_count == 1:
    #         flash('邮箱已存在','err')
    #         return redirect(url_for('home.user'))
    #
    #     phone_count = User.query.filter_by(phone=data['phone']).count()
    #     if data['phone'] != user_s.phone and phone_count == 1:
    #         flash('手机号已存在', 'err')
    #         return redirect(url_for('home.user'))
    #
    #     user_s.email = data['email']
    #     user_s.phone = data['phone']
    #     user_s.info = data['info']
    #     db.session.add(user_s)
    #     db.session.commit()
    #     flash('修改成功','ok')
    #     return redirect(url_for('home.user'))
    # return render_template('home/user.html',form=form,user_s=user_s)
    return render_template('home/user.html')

# 修改密码
@home.route('/pwd/')
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        if not user.check_pwd(data['old_pwd']):
            flash('旧密码错误','err')
            return redirect(url_for('home.pwd'))
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功，请重新登录','ok')
        return redirect(url_for('home.logout'))
    return render_template('home/pwd.html',form=form)

# 个人所有评论
@home.route('/comments/<int:page>')
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == Comment.movie_id,
                                                            User.id == session['user_id']).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('home/comments.html',page_data=page_data)

# 会员登录日志
@home.route('/loginlog/<int:page>',methods=['GET'])
def loginlog(page):
    if page is None:
        page= 1
    page_data = Userlog.query.filter_by(
        user_id=int(session['user_id'])
        ).order_by(Userlog.addtime.desc()
        ).paginate(page=page,per_page=10)


    return render_template('home/loginlog.html',page_data=page_data)

# 电影收藏
@home.route('/moviecol/')
def moviecol():

    return render_template('home/moviecol.html')

# 首页面重定向
@home.route('/')
def index_redict():
    return redirect(url_for('home.index',page=1))

# 首页
@home.route('/<int:page>/')
def index(page=None):
    tags = Tag.query.all()
    # 标签
    tid = request.args.get('tid',0)
    tid = int(tid)
    page_data = Movie.query
    if tid != 0:
        page_data=page_data.filter_by(tag_id=tid)
    # 星级
    star = request.args.get('star',0)
    star = int(star)
    if star != 0:
        page_data = page_data.filter_by(star=star)
    # 时间
    time = request.args.get('time',0)
    time = int(time)
    if time != 0:
        if time == 1:
            # 降序
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        if time == 2:
            # 升序
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )
    # 播放量
    pm = request.args.get('pm',0)
    pm = int(pm)
    if pm != 0:
        if pm == 1:
            # 降序
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        if pm == 2:
            # 升序
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )
    # 评论量
    cm = request.args.get('cm',0)
    cm = int(cm)
    if cm != 0:
        if cm == 1:
            # 降序
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        if cm == 2:
            # 升序
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page= 1
    page_data = page_data.paginate(page=page,per_page=10)
    p=dict(
        tid=tid,
        star = star,
        time = time,
        pm=pm,
        cm=cm,
    )
    return render_template('home/index.html',tags=tags,p=p,page_data=page_data)



# 轮播图动画
@home.route('/animation/')
def animation():
    data = Preview.query.all()

    return render_template('home/animation.html',data=data)

# 添加搜索
@home.route('/search/<int:page>')
def search(page):
    if page is None:
        page=1
    key = request.args.get('key','')
    movie_count = Movie.query.filter(Movie.title.ilike("%"+key+'%')).count()
    page_data = Movie.query.filter(
        Movie.title.ilike("%"+key+'%')
    ).order_by(Movie.addtime.desc()).paginate(page=page,per_page=10)



    return render_template('home/search.html',key=key,page_data=page_data,movie_count=movie_count)


# 播放页面
@home.route('/play/<int:id>/<int:page>',methods=['GET','POST'])
def play(id=None,page=None):

    movie = Movie.query.join(Tag).filter(Tag.id==Movie.tag_id,Movie.id==int(id)).first_or_404()

    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == movie.id,
                                                            User.id == Comment.user_id).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    movie.playnum = movie.playnum + 1
    form = CommentForm()
    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['content'],
            movie_id = movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum +1
        flash('添加评论成功','ok')
        return redirect(url_for('home.play',id=movie.id,page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html',movie=movie,form=form,page_data=page_data)






