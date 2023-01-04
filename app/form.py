from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class LoginForm(FlaskForm):
     username = StringField("Tên đăng nhập",validators=[DataRequired()])
     password = PasswordField("Mật khẩu", validators=[DataRequired()])
     remember = BooleanField("Ghi nhớ")
     submit = SubmitField("Đăng nhập")

class InsertForm(FlaskForm):
     userid = StringField("ID", validators=[DataRequired()])
     role = StringField("Chức vụ",validators=[DataRequired()])
     email = StringField("Email",validators=[DataRequired()])
     username = StringField("Tên Nhân Viên", validators=[DataRequired()])
     ngquanly = StringField("Người quản lý",validators=[DataRequired()])
     password = PasswordField('Mật khẩu', validators=[DataRequired()])
     submit = SubmitField("Thêm nhân viên")
     
class UpdateForm(FlaskForm):
     id = StringField("ID", validators=[DataRequired()])
     username = StringField("Tên Nhân Viên")
     role = StringField("Chức vụ")
     email = StringField("Email")
     ngquanly = StringField("Người quản lý")
     password = PasswordField('Mật khẩu')
     submit = SubmitField("Update nhân viên")

class UpLoadForm(FlaskForm):
     fileup = FileField('Chọn file bạn muốn tải lên', validators=[FileRequired()])
     submit_upload = SubmitField('Upload file')
      
class DownloadForm(FlaskForm):
     file_id = StringField('Nhập tên file', validators=[DataRequired()])
     submit_download = SubmitField('Donwload file')
