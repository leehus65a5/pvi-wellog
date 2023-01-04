from app import app, db
from app.model import User
from flask import redirect, url_for, render_template, request, flash, session, g
from app.form import LoginForm
from werkzeug.security import check_password_hash

#định nghĩa public function cho phép người ngoài chưa đăng nhập có thể view
def public_route(decorated_function):
    decorated_function.is_public = True
    return decorated_function

# lưu thông tin của user vào g.user
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
     #    return redirect(url_for('login'))
    else:
        get_user_info = db.session.execute(db.select(User).where(User.id == user_id)).fetchone()
        g.user = get_user_info


#chặn tất cả những người dùng chưa đăng nhập vào các trang không hợp lệ
#chỉ cho phép các tài khoản đã login có thể truy cập nội dung trang web
@app.before_request
def check_route_access():
     if not request.endpoint:
          print('no request')
          return
     elif any([request.endpoint.startswith('static'), g.user,  getattr(app.view_functions[request.endpoint],'is_public',False)]):
          return 
     else:
          return redirect(url_for('login'))

@app.route('/')
@app.route('/index', methods=['GET','POST'])
@public_route
def index():
     return render_template('index.html')

#public page.
@app.route('/login', methods=['POST','GET'])
@public_route
def login():
     form = LoginForm()
     if form.validate_on_submit() and request.method == 'POST':
          username = form.username.data
          password = form.password.data
          check = db.session.execute(db.select(User).where(User.username==username)).fetchone()
          
          if not check or not check_password_hash(check.User.password, password):
               flash('Thông tin đăng nhập không chính xác')
               redirect('login.html')
          else:
               flash('Đăng nhập thành công')
               session.clear()
               session['user_id'] = check.User.id
               
               get_id = str(check.User.id).lower()
               if get_id.startswith('ad'):
                    return redirect(url_for('admin.dashboard', user_id = get_id))
               elif get_id.startswith('dm'):
                    return redirect(url_for('datamanager.dashboard'))
               elif get_id.startswith('da'):
                    return redirect(url_for('datamanager.dashboard'))
               return redirect(url_for('user.dashboard'))
          
     return render_template('login.html',form=form)

@app.route('/logout')
def logout():
     session.clear()
     flash('Đăng xuất thành công')
     return redirect(url_for('login'))

@app.route('/test')
def test():
     userList = db.session.query(User).all()
     userList = [(i.id, i.username, i.password) for i in userList]
     check = db.session.query(User).all()
     return render_template('test.html', user=userList, check = check)

# @app.router('/dash1/')
# @public_route

# @app.route('/user/<name>')
# def user(name):
#      return "<h1> hello user {} </h1>".format(name)

# @app.route('/admin/<name>')
# def admin(name):
#      return "<h1> hello admin {} </h1>".format(name)

# @app.route('/datamanage/<name>')
# def datamanage(name):
#      return "<h1> hello datamanage {} </h1>".format(name)


