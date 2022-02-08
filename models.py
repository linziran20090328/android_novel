from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from flask_login import UserMixin, current_user

tb_user_collection = db.Table(
    "info_user_collection",
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),  # 文章编号
    db.Column("info_nobel", db.Integer, db.ForeignKey("info_nobel.id"), primary_key=True),  # 分类编号
    db.Column("create_time", db.DateTime, default=datetime.now)  # 收藏创建时间
)
tb_user_novel_view_records = db.Table(
    "info_user_novel_view_records",
    db.Column("user_id", db.Integer, db.ForeignKey("info_user.id"), primary_key=True),  # 文章编号
    db.Column("info_nobel", db.Integer, db.ForeignKey("info_nobel.id"), primary_key=True),
)


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class User(db.Model, UserMixin, BaseModel):
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
    collection_news = db.relationship("News", secondary=tb_user_collection, lazy="dynamic")  # 用户收藏的文章
    novel_view_records = db.relationship('Nobel', secondary=tb_user_novel_view_records, lazy="dynamic", backref='user')

    def set_password_hash(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


class NovelClassification(BaseModel, db.Model):
    __tablename__ = "info_nobel_classification"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    nobel = db.relationship('Nobel', backref='novel_classification')


class Nobel(BaseModel, db.Model):
    """文章"""
    __tablename__ = "info_nobel"

    id = db.Column(db.Integer, primary_key=True)  # 文章编号
    title = db.Column(db.String(256), nullable=False)  # 文章标题
    source = db.Column(db.String(64), nullable=False)  # 文章来源
    digest = db.Column(db.String(512), nullable=False)  # 文章摘要
    content = db.Column(db.Text, nullable=False)  # 文章内容
    index_image_url = db.Column(db.String(256))  # 文章列表图片路径
    nobel_id = db.Column(db.Integer, db.ForeignKey("info_nobel.id"))


if __name__ == '__main__':
    NovelClassification.nobel.filter(Nobel.user.nick_name == current_user.nick_name).first()
