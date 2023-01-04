from app import db, app
from sqlalchemy import select


with app.app_context():
     db.reflect()

class User(db.Model):
     __table__ = db.metadata.tables['users']
     
     def creatUser(self):
          get_id = "".join(self.id)
          list_id = [str(i[0]).lower() for  i in db.session.execute(select(User.id)).fetchall()]
          if get_id in list_id:
               return 'User đã tồn tại trong database', False
          db.session.add(self)
          db.session.commit()
          return 'Tạo User thành công', True

     def updateUser(**args):
          get_id = args['id']
          get_user = User.query.filter_by(id = get_id).first()
          if not get_user:
               return 'Không tồn tại User', False
          for att in args:
               if att != 'id':
                    if hasattr(get_user, att):
                         setattr(get_user, att, args[att])
          try:
               db.session.commit()
          except:
               return f'Update failse hãy thử lại', False
          return f'Update thành công User {args["username"]}', True
     
     def deleteUser(user_id):
          get_user = User.query.filter_by(id = user_id).first()
          if not get_user:
               return 'Không tồn tại User', False
          try:
               User.query.filter_by(id = user_id).delete()
               db.session.commit()
          except:
               return 'error in delete user', False
          return f'Delete user thành công {user_id}', True
     
     def __repr__(self):
        return f'User({self.id} : {self.username})'

class Files(db.Model):
     __table__ = db.metadata.tables['files']
     
     def upFile(self):
          get_id = "".join(self.id)
          list_id = [i[0] for i in db.session.execute(select(Files.id)).fetchall()]
          if get_id in list_id:
               return False, 'Upload file thất bại'
          db.session.add(self)
          db.session.commit()
          return True, 'Upload file thành công'
     
     def downloadFile(file_id):
          get_file = Files.query.filter_by(id = file_id).first()
          if not get_file:
               return False
          return get_file
          
     def __repr__(self) -> str:
          return f'File = ({self.id} : {self.filename})'

class A10(db.Model):
     __table__ = db.metadata.tables['a10']
     
     def to_dict(self):
          return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Udata(db.Model):
     __table__ = db.metadata.tables['truycapdata']

class Files2(db.Model):
     __table__ = db.metadata.tables['files2']
     
class FileLog(db.Model):
     __table__ = db.metadata.tables['filelog']