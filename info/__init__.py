import os

from flask import Flask

from configs import config
from extensions import db
from common.utils import setup_log


def create_app(config_name=None):
    app = Flask('项目名称')

    if not config_name:
        # 没有没有传入配置文件，则从本地文件读取
        config_name = os.getenv('FLASK_CONFIG', 'development')
    setup_log(config_name)
    app.config.from_object(config[config_name])

    # 注册插件
    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
