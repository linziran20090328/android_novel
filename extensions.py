from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from common.redis_utils import RedisStore
# from models import User
# from common.redis_utils import RedisStore
from common.utils import AnonymousUser
# from flask import session

db = SQLAlchemy()
migrate = Migrate()
redis_store = RedisStore()
login_manager = LoginManager()
# 需要权限的页面重定向到首页
login_manager.login_view = '重定向的'
login_manager.anonymous_user = AnonymousUser

from models import User


# 用于获取用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)