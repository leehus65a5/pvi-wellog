from app import db, mySql, tools, app
from app.model import User, Udata, Files2, FileLog, Files
from flask import render_template, url_for, flash, redirect, g, request,session, send_file
from werkzeug.utils import secure_filename
from app.admin import admin
import csv, os
from io import BytesIO
from app.form import InsertForm, UpdateForm, UpLoadForm, DownloadForm
from werkzeug.security import generate_password_hash
from sqlalchemy import select, or_,and_

#Chỉ cho phép Admin có thể truy cập vào blueprint admin
@admin.before_request
def check_auth():
     if g.user:
          if not str(g.user.User.id).lower().startswith('ad'):
               return redirect(url_for('index'))

@admin.route('/')
@admin.route('/dashboard')
def dashboard():
     return render_template('admin/base.html')

@admin.route('/manage', methods=['GET','POST'])
def quan_ly_nhan_vien():
     add_form = InsertForm()
     edit_form = UpdateForm()
     users = db.session.execute(select(User)).fetchall()
     get_all_user = User.query.all()
     print(users)
     if add_form.validate_on_submit() and request.method == 'POST':
          passw = generate_password_hash(add_form.password.data)
          new_user = User(id=add_form.userid.data,
                         role=add_form.role.data,
                         email=add_form.email.data,
                         username=add_form.username.data,
                         ngquanly=add_form.ngquanly.data,
                         password=passw)
          mess, flag = new_user.creatUser()
          if not flag:
               mess = 'có lỗi khi nhập dữ liệu'
          flash(mess)
          return redirect(url_for('admin.quan_ly_nhan_vien'))

     if request.method == 'POST' and edit_form.validate_on_submit():
          print(edit_form.data)
          print('----------------')
          update = {}
          for i in User.__table__.columns:
               if edit_form.data[i.key]:
                    update[i.key] = edit_form.data[i.key]
          print(update)
          mess = User.updateUser(**update)[0]
          flash(mess)
          return redirect(url_for('admin.quan_ly_nhan_vien'))

     if request.method == 'POST':
          details = request.form
          user_id = details['user_id']
          mess = User.deleteUser(str(user_id))[0]
          flash(mess)
          return redirect(url_for('admin.quan_ly_nhan_vien'))
          
     return render_template('admin/manage.html', users_add=users, users_edit = get_all_user, edit_form = edit_form, add_form = add_form)

# @admin.route('/update', methods=['GET', 'POST'])
# def update_nhan_vien():
#      get_all_user = User.query.all()
#      form = UpdateForm()
#      if request.method == 'POST' and form.validate_on_submit():
#           print(form.data)
#           print('----------------')
#           update = {}
#           for i in User.__table__.columns:
#                if form.data[i.key]:
#                     update[i.key] = form.data[i.key]
#           print(update)
#           mess = User.updateUser(**update)[0]
#           flash(mess)
#           return redirect(url_for('admin.update_nhan_vien'))
#      return render_template('admin/update.html', users=get_all_user, form = form)

# @admin.route('/delete', methods = ['GET','POST'])
# def delete_nhan_vien():
#      get_all_user = User.query.all()
#      if request.method == 'POST':
#           details = request.form
#           user_id = details['user_id']
#           mess = User.deleteUser(str(user_id))[0]
#           flash(mess)
#           return redirect(url_for('admin.delete_nhan_vien'))
          
#      return render_template('admin/delete.html', users=get_all_user)

#-------------CHECK ZONE CODE----------------------

@admin.route('/test', methods=['GET','POST'])
def test():
    return render_template('admin/test.html')


def check():
     #this is code how we can connect to the mysql databases
     cur = mySql.connection.cursor()
     cur.execute('select * from a10')
     rs = ''
     for i in range(20):
          rs += str(cur.fetchone()) + '<br>'
     
     rt = db.engine.execute('select * from users')
     rtt = ''
     for i in rt:
          rtt += str(i) + '<br>'
     
     a10 = db.Table('a10', db.metadata, autoload=True,autoload_with=db.engine)
     check33 = db.session.query(a10).all()
     cxx, k = '', 0
     for i in check33:
          cxx += str(i.DEPT) + '<br>'
          k += 1
          if k == 10:
               break
     
     # with app.app_context():
     #      Dean = Base.classes.dean
     #      cxx1 = db.session.query(Dean).all()
     #      x1 = ''
     #      for i in cxx1:
     #           x1 += str(i.DDIEM_DA) + '<br>'
     
     x1 = 'close'
     
     return f'<p> {rtt} </p> <h2> check </h2> <p> {x1} </p> <h2> check2 </h2> <p> {cxx} </p>'
