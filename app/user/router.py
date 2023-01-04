import json
from app import db, mySql, app
from flask import render_template, url_for, flash, redirect, g, request, jsonify, session
from app.user import user
from app.model import A10, Udata, Files2, FileLog, Files
from sqlalchemy import select, and_
from app.form import UpLoadForm
from app import tools
from werkzeug.utils import secure_filename
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import mapper
import csv, os
import pandas as pd
import json



@user.route('/')
@user.route('/dashboard')
def dashboard():
    return render_template('user/base.html')


@user.route('/test', methods=['GET', 'POST'])
def showdata():
     a10_data2 = A10.query.all()
     x = a10_data2[0]
     listkey = x.__dict__.keys()
     listkey = sorted(listkey)[1:-1]
     # d = []
     
     uid = session.get('user_id')
     listTable = db.session.execute(select(Udata.tableid).where(Udata.userid == uid))
     listTable = [i.tableid for i in listTable]
     
     if request.method == 'POST':
          form = request.form
          if 'all' not in form:
               cols = [i for i in form if i not in ['start', 'stop','all','save']]
               sql = select(A10.DEPT,*[getattr(A10, i) for i in cols]).where(and_(A10.DEPT >= form['start'], A10.DEPT <= form['stop']))
               r = db.session.execute(sql).fetchall()
               a10_data2 = r
               
          return render_template('user/test.html', datas = a10_data2, listkey = listkey, listTable = listTable)
     
     # for i in a10_data2:
     #      d.append(i.to_dict())
          
     # path1 = os.path.join(app.root_path, 'user/static/files/', 'saveFiles.csv')
     # print(path1)
     # with open(path1, 'w', newline='') as f:
     #      dict_writer = csv.DictWriter(f, d[0].keys())
     #      dict_writer.writeheader()
     #      dict_writer.writerows(d)
     
     print(type(a10_data2[0]))
     print(a10_data2[0])
     print(a10_data2[0].__dict__)
     print(sorted(a10_data2[0].__dict__))
     
     return render_template('user/test.html', datas = a10_data2, listkey = listkey, listTable = listTable)

@user.route('/upload', methods = ['GET','POST'])
def uploadfiles2():
     
     form = UpLoadForm()
     list_file_send = select(Files2.uploader,Files2.reviewer, Files2.wellid, Files2.status).where(Files2.uploader == g.user.User.id)
     get_list_send = db.session.execute(list_file_send).fetchall()
     
     list_hist = select(FileLog.uploader, FileLog.reviewer, FileLog.wellid, FileLog.status).where(FileLog.uploader == g.user.User.id)
     get_list_hist = db.session.execute(list_hist).fetchall()
     
     print(get_list_send, get_list_hist)
     
     print('uid', g.user.User.id)
     print('role', g.user.User.role)
     
     print(request.form)
     if form.validate_on_submit() and request.method == 'POST':
          file1 = form.fileup.data
          # file1 = request.files['fileup']
          file1_data = request.files['fileup'].read()
          file1.stream.seek(0)
          # file1.save(os.path.join(os.getcwd(), 'app' ,app.config['UPLOAD_FOLDER'],secure_filename(file1.filename)))
          path = os.path.join(app.root_path, 'static', 'files', secure_filename(file1.filename))
          file1.save(path)
          print('path = ' , path)
          curinfo, wellinfo, df = tools.convert_lasio(path)
          fileUp = Files2(
               uploader = g.user.User.id,
               reviewer = g.user.User.ngquanly,
               wellid = file1.filename.split('.')[0],
               cur_info = curinfo,
               well_info = wellinfo,
               data = df.to_json(),
               status = 'pending',
          )
          db.session.add(fileUp)
          db.session.commit()         
          print('ok here')
          return redirect(url_for('user.uploadfiles2'))
          
     return render_template('user/upload.html', form=form, sendfiles = get_list_send, hist = get_list_hist) 

@user.route('/data_well_log', methods=['GET', 'POST'])
def check():
     
     uid = session.get('user_id')
     listTable = db.session.execute(select(Udata.tableid).where(Udata.userid == uid))
     listTable = [i.tableid for i in listTable]
     print(uid)
     print(listTable)
     
     data = None
     listk = None
     form = request.form
     check_table = session.get('table')
     
     print('check table', check_table)
     
     if 'name' not in form and not check_table:
          print('no name and check table')
          return render_template('user/data_well_log.html', datas = None, listkey = None, listTable = listTable )
     print('here')
     
     
     if request.method == 'POST':
          if 'name' in form and len(form['name']) >= 1:
               session['table'] = form['name']
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               data = db.session.execute(select(tb_cls)).fetchall()
               listk = [i.name for i in tb_cls.columns]
               listk = sorted(listk)
               print('check1')
               print(session['table'])
               # return render_template('user/check.html', datas = data, listkey = listk)
          elif 'start' in form:
               print('check 2 name not in table, get selected collums')
               print(form)
               listk = [i for i in form if i not in ['start', 'stop']]
               print(listk)
               
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               sql = select(*[getattr(tb_cls.c, i) for i in listk]).where(
                    and_(tb_cls.c.DEPT >= form['start'], tb_cls.c.DEPT <= form['stop']))
               data = db.session.execute(sql).fetchall()
               
               print('check2')
               # return render_template('user/check.html', datas = data, listkey = listk)
          else:
               tb_cls = db.Table(session['table'], db.metadata,autoload=True,autoload_with=db.engine)
               data = db.session.execute(select(tb_cls)).fetchall()
               listk = [i.name for i in tb_cls.columns]
               listk = sorted(listk)
               print(listk)
               print('check3')
               # return render_template('user/check.html', datas = data, listkey = listk)
          
          print('check4')
          
     # a10 = db.Table('a10', db.metadata,autoload=True,autoload_with=db.engine)
     # sql = select(a10)
     # r = db.session.execute(sql).fetchall()
     # for i in r:
     #      print(i)
     
     print('chech5')
     return render_template('user/data_well_log.html', datas = data, listkey = listk, listTable = listTable)

@user.route('/plot')
def plot():
     return render_template('user/plotdata.html')

@user.route('/test2', methods=['GET', 'POST'])
def test():
     print('we are in test')
     uid = session.get('user_id')
     listTable = db.session.execute(select(Udata.tableid).where(Udata.userid == uid))
     listTable = [i.tableid for i in listTable]
     print(uid)
     print(listTable)
     
     a10 = db.Table('a10', db.metadata , autoload=True, autoload_with=db.engine)
     sql = select(a10)
     print('sql = ' , sql)
     dataframe = pd.read_sql_query(sql, db.engine)
     print('dataframe = ',  dataframe)
     js_data = dataframe.to_json(orient="records")
     js_data2 = dataframe.to_json()
     return render_template('user/test2.html', listTable = listTable, js_data = js_data, js_data2 = js_data2)

@user.route('/kiemtra', methods = ['GET','POST'])
def kiemtra():
     cls = select(Files2.data).where(and_(Files2.wellid == 'A8', Files2.uploader == 'AD001'))
     print(cls)
     results = db.session.execute(cls).fetchone()
     print('check type of results',type(results[0]))
     get_js = json.loads(results[0])
     print(type(get_js))
     df = pd.read_json(results[0])
     print(type(df))
     print(df)
     return render_template('user/kiemtra.html')