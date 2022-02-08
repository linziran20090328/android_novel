import redis
from redis import StrictRedis
from configs import config
from common import constants


class RedisStore:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

        self.strict_redis: StrictRedis = None

    def init_app(self, app):
        # 配置 redis 数据库
        if 'REDIS_HOST' not in app.config:
            raise Exception('需要先加载redis配置信息')
        self.strict_redis = StrictRedis(host=app.config['REDIS_HOST'],
                                        port=app.config['REDIS_PORT'],
                                        decode_responses=True)
        setattr(app, 'strict_redis', self.strict_redis)

    def store_chapter_image(self, code_id, text):
        self.strict_redis.setex("ImageCode_" + code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)