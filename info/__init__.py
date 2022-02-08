import os

from flask import Flask

from configs import config
from extensions import db, migrate, login_manager, redis_store
from common.utils import setup_log
import pymysql


def create_app(config_name=None):
    pymysql.install_as_MySQLdb()
    app = Flask('andorid_novel')

    if not config_name:
        # 没有没有传入配置文件，则从本地文件读取
        config_name = os.getenv('FLASK_CONFIG', 'development')
    setup_log(config_name)
    app.config.from_object(config[config_name])

    # 注册插件
    register_extensions(app)
    register_blueprint(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    redis_store.init_app(app)


def register_blueprint(app: Flask):
    from info.index import index_bp
    from info.auth import auth_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
