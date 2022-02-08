from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from flask_login import UserMixin

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

class User(db.Model, UserMixin,BaseModel):
    __tablename__ = 'info_user'
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    mobile = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    avatar_url = db.Column(db.String(256))  # 用户头像路径
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)
    signature = db.Column(db.String(512))  # 用户签名
    gender = db.Column(  # 用户性别
        db.Enum(
            "MAN",  # 男
            "WOMAN"  # 女
        ),
        default="MAN")
    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

class Nobel(BaseModel, db.Model):
    __tablename__ = "info_nobel"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名

class News(BaseModel, db.Model):
    """文章"""
    __tablename__ = "info_news"

    id = db.Column(db.Integer, primary_key=True)  # 文章编号
    title = db.Column(db.String(256), nullable=False)  # 文章标题
    source = db.Column(db.String(64), nullable=False)  # 文章来源
    digest = db.Column(db.String(512), nullable=False)  # 文章摘要
    content = db.Column(db.Text, nullable=False)  # 文章内容
    index_image_url = db.Column(db.String(256))  # 文章列表图片路径
    nobel_id = db.Column(db.Integer, db.ForeignKey("info_nobel.id"))

