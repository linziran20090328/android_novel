import logging
import os
import sys


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = ""

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    LOG_LEVEL = logging.DEBUG


class DevelopmentConfig(BaseConfig):
    """开发配置"""
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/info"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """测试配置"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/info"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = logging.ERROR


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}