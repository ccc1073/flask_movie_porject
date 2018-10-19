from . import admin
from flask import render_template, url_for, redirect, flash, session, request,abort
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm, PwdForm, AuthForm, RoleForm, AdminForm
from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth, Role
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os
import uuid, datetime


# 上下文应用处理器
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime(('%Y-%m-%d %H:%M:%S'))
    )
    return data

# 管理员登录装饰器
def admin_login_rep(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session or session['admin'] is None:
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)

    return decorated_function
# 权限控制装饰器
def admin_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(Role).filter(Role.id==Admin.role_id,
                                              Admin.id==session['admin_id']).first()
        if admin.is_super == 0:
            return func(*args, **kwargs)
        # 查询出该管理员下有什么权限
        auths = admin.role.auths
        # 分割成列表
        auths = list(map(lambda v:int(v),auths.split(',')))
        # 查询所有权限
        auth_list = Auth.query.all()
        # 历遍权限列表 和 该管理员所拥有的权限列表 将两者进行比较 在拥有相同权限id的情况下获取出权限地址
        urls = [v.url for v in auth_list for val in auths if val==v.id]

        rule = request.url_rule

        if str(rule) not in urls:
            abort(404)

        return func(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route('/')
@admin_login_rep
def index():
    return render_template('admin/index.html')


# 登录
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        data = form.data
        print(data)
        admin = Admin.query.filter_by(name=data['account']).first()

        if not admin.check_pwd(data['pwd']):
            # 消息的闪现
            flash('密码错误', 'err')
            return redirect(url_for('admin.login'))
        # 密码正确存入session中
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        # 添加管理员登录日志
        adminloginlog = Adminlog(
            admin_id=admin.id,
            ip=request.remote_addr,
        )
        db.session.add(adminloginlog)
        db.session.commit()

        return redirect(request.args.get('next') or url_for('admin.index'))

    return render_template('admin/login.html', form=form)


# 退出
@admin.route('/logout/')
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))

# 修改密码
@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_rep
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        admin = Admin.query.filter_by(name=session['admin']).first()
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功,请重新登录', 'ok')
        redirect(url_for('admin.logout'))

    return render_template('admin/pwd.html', form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_rep
def tag_list(page):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/tag_list.html', page_data=page_data)


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        tag = Tag.query.filter_by(name=data['name']).count()
        if tag == 1:
            flash('名称已存在', 'error')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'ok')
        # 添加操作日志
        oplog = Oplog(
            admin_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加标签%s' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


# 删除标签
@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_rep
@admin_auth
def tag_del(id):
    tag = Tag.query.get(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 编辑标签
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def tag_edit(id):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        print(data)
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1:
            flash('名称已存在', 'error')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.name = tag['name']
        db.session.add(tag)
        db.session.commit()
        flash('修改标签成功', 'ok')
        return redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 添加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + url)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']

        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie/list/<int:page>', methods=['GET'])
@admin_login_rep
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(Tag.id == Movie.id).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def movie_del(id=None):
    movie = Movie.query.get_or_404(int(id))
    db.session.delete(movie)
    db.session.commit()
    flash('删除电影成功', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


# 编辑电影 暂时pass 原理同编辑标签

# 添加预告
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + logo)
        preview = Preview(
            title=data['title'],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加预告成功', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 预告列表
@admin.route('/preview/list/<int:page>')
@admin_login_rep
def preview_list(page):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/preview_list.html', page_data=page_data)


# 删除预告
@admin.route('/preview/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def preview_del(id):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash('删除预告成功', 'ok')

    return redirect(url_for('admin.preview_list', page=1))


# 修改预告暂时pass 同理其他修改

# 会员列表
@admin.route('/user/list/<int:page>', methods=['GET'])
@admin_login_rep
def user_list(page):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/user_list.html', page_data=page_data)


# 会员详情
@admin.route('/user/view/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def user_view(id=None):
    user = User.query.get_or_404(id)
    return render_template('admin/user_view.html', user=user)


# 会员删除
@admin.route('/user/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def user_del(id):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash('删除会员成功', 'ok')

    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list/<int:page>', methods=['GET'])
@admin_login_rep
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(Movie.id == Comment.movie_id,
                                                            User.id == Comment.user_id).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/comment_list.html', page_data=page_data)


# 删除评论
@admin.route('/comment/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def comment_del(id):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功', 'ok')

    return redirect(url_for('admin.comment_list', page=1))


# 收藏列表
@admin.route('/moviecol/list/<int:page>', methods=['GET'])
@admin_login_rep
@admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).join(User).filter(Movie.id == Moviecol.movie_id,
                                                             User.id == Moviecol.user_id).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 删除收藏
@admin.route('/moviecol/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def moviecol_del(id):
    moviecol = Moviecol.query.get_or_404(int(id))
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除收藏成功', 'ok')

    return redirect(url_for('admin.moviecol_list', page=1))


# 管理员登录日志
@admin.route('/adminloginlog/list/<int:page>', methods=['GET'])
@admin_login_rep
def adminloginlog_list(page):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(Admin).filter(Admin.id == Adminlog.admin_id, ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/adminloginlog_list.html', page_data=page_data)


# 操作日志列表
@admin.route('/oplog/list/<int:page>', methods=['GET'])
@admin_login_rep
def oplog_list(page):
    if page is None:
        page = 1
    page_data = Oplog.query.join(Admin).filter(Admin.id == Oplog.admin_id, ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/oplog_list.html', page_data=page_data)


# 会员登录日志
@admin.route('/userloginlog/list/<int:page>', methods=['GET'])
@admin_login_rep
def userloginlog_list(page):
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(User.id == Userlog.user_id, ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/userloginlog_list.html', page_data=page_data)


# 角色添加
@admin.route('role/add/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda v: str(v), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功', 'ok')
    return render_template('admin/role_add.html', form=form)


# 角色删除
@admin.route('/role/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def role_del(id):
    role = Role.query.get_or_404(int(id))
    db.session.delete(role)
    db.session.commit()
    flash('删除角色成功', 'ok')

    return redirect(url_for('admin.role_list', page=1))

#角色编辑pass 同理
# form.auths.data 赋值以后可以 在渲染页面自动显示赋值的数据

# 角色列表
@admin.route('role/list/<int:page>', methods=['GET'])
@admin_login_rep
@admin_auth
def role_list(page):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/role_list.html', page_data=page_data)


# 权限添加
@admin.route('/auth/add/', methods=['GET', 'POST'])
@admin_login_rep
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash('添加权限成功', 'ok')
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>', methods=['GET'])
@admin_login_rep
@admin_auth
def auth_list(page):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/auth_list.html', page_data=page_data)


# 权限编辑暂时pass 同理

# 权限删除
@admin.route('/auth/del/<int:id>', methods=['GET'])
@admin_login_rep
@admin_auth
def auth_del(id):
    auth = Auth.query.get_or_404(int(id))
    db.session.delete(auth)
    db.session.commit()
    flash('删除权限成功', 'ok')

    return redirect(url_for('admin.auth_list', page=1))

# 添加管理员
@admin.route('/admin/add',methods=['GET','POST'])
@admin_login_rep
@admin_auth
def admin_add():
    form = AdminForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        admin = Admin(
            name=data['name'],
            pwd = generate_password_hash(data['pwd']),
            role_id = data['role_id'],
            is_super = 1
        )
        db.session.add(admin)
        db.session.commit()
        flash('添加管理员成功', 'ok')
    return render_template('admin/admin_add.html',form=form)

# 管理员列表
@admin.route('/admin/list/<int:page>',methods=['GET'])
@admin_login_rep
@admin_auth
def admin_list(page):
    if page is None:
        page = 1
    page_data = Admin.query.join(Role).filter(Role.id==Admin.role_id).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)

    return render_template('admin/admin_list.html',page_data=page_data)
