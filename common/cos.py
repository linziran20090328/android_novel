from datetime import date
from qcloud_cos import CosConfig, CosS3Client
from os import getenv
from common import constants

class TenCos:
    def __init__(self):
        secret_id = getenv('secret_id')  # 替换为用户的 secretId
        secret_key = getenv('secret_key')  # 替换为用户的 secretKey
        region = getenv('region')
        config = CosConfig(Region=region,  # 替换为用户的 Region
                           SecretId=secret_id,
                           SecretKey=secret_key)
        # 2. 获取客户端对象
        self.client = CosS3Client(config)

    def save_user_pic(self, filename, file, default_path='bbs'):
        filename = "/".join([default_path, date.today().strftime('%Y-%m'), filename])
        file_url = constants.COS_ACCESS_URL + filename
        response = self.client.put_object(
            Bucket=constants.COS_BUCKET,
            Body=file,
            Key=filename,
            EnableMD5=False
        )
        if response['ETag']:
            return 'ok', file_url
        else:
            return '', ''
