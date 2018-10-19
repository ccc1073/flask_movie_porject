from app import app
from flask_migrate import Migrate,MigrateCommand
from app import db
from flask_script import Manager
from app.models import Admin,Role,User
from werkzeug.security import generate_password_hash
import uuid

manager = Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    # app.run(host='127.0.0.1',port=5000)
    manager.run()
    # user = User(
    #     name='kumu',
    #     pwd=generate_password_hash("789456"),
    #     email='1qe234@qq.com',
    #     phone='13803112068',
    #     info='巴拉巴拉巴拉巴拉',
    #     face='1111.jpg',
    #     uuid=uuid.uuid4().hex
    # )
    # db.session.add(user)
    # db.session.commit()

    # role = Role(
    #     name='超级管理员1',
    #     auths=' '
    # )
    # db.session.add(role)
    # db.session.commit()
    # from werkzeug.security import generate_password_hash
    # admin = Admin(
    #     name = 'imoocmovie1',
    #     pwd = generate_password_hash("789456"),
    #     is_super = 0,
    #     role_id = 1
    # )
    # db.session.add(admin)
    # db.session.commit()