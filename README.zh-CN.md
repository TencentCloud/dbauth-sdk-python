语言 : [🇺🇸](./README.md) | 🇨🇳
<h1 align="center">Tencent Cloud DBAuth SDK</h1>
<div align="center">
欢迎使用腾讯云数据库CAM验证SDK，该SDK为开发者提供了支持的开发工具，以访问腾讯云数据库CAM验证服务，简化了腾讯云数据库CAM验证服务的接入过程。
</div>

### 依赖环境

1. 依赖环境：Python 3.6 版本及以上。
2. 使用前需要在腾讯云控制台启用CAM验证。
3. 在腾讯云控制台[账号信息](https://console.cloud.tencent.com/developer)
   页面查看账号APPID，[访问管理](https://console.cloud.tencent.com/cam/capi)页面获取 SecretID 和 SecretKey 。

### 通过pip安装

您可以通过 pip 安装方式将腾讯云数据库CAM Python SDK 安装到您的项目中。
请在命令行中执行以下命令:

```bash
pip install git+https://github.com/TencentCloud/dbauth-sdk-python.git
```

请注意，如果同时有 python2 和 python3 环境， python3 环境需要使用 pip3 命令安装。

#### 间接依赖项

tencentcloud-sdk-python 3.0.1224版本及以上。

### 示例 - 连接到数据库实例

```
import logging
import os
import time

import pymysql
from dbauth.db_authentication import DBAuthentication
from dbauth.model.generate_authentication_token_request import GenerateAuthenticationTokenRequest
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

# 配置root logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(threadName)s] - {%(module)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger(__name__)


def main():
    region = "ap-guangzhou"
    instance_id = "cdb-123456"
    user_name = "camtest"
    host = "gz-cdb-123456.sql.tencentcdb.com"
    port = 25925
    db_name = "test"
    secret_id = os.environ['AK']
    secret_key = os.environ['SK']

    connection = None
    try:
        # 获取连接
        connection = get_db_connection_using_cam(secret_id, secret_key, region,
                                                 instance_id, user_name, host, port, db_name)

        # 验证连接是否成功
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Success!';")
            result = cursor.fetchone()
            log.info(result[0])  # 应该打印 "Success!"
    except Exception as e:
        log.error(f"An error occurred: {e}")
    finally:
        if connection and connection.open:
            connection.close()


def get_db_connection_using_cam(secret_id, secret_key, region, instance_id, user_name, host, port, db_name):
    cred = credential.Credential(secret_id, secret_key)

    max_attempts = 3
    last_exception = None
    for attempt in range(1, max_attempts + 1):
        try:
            auth_token = get_auth_token(region, instance_id, user_name, cred)

            connection = pymysql.connect(
                host=host,
                port=port,
                user=user_name,
                password=auth_token,
                database=db_name
            )
            return connection
        except Exception as e:
            last_exception = e
            log.info(f"Attempt {attempt} failed.")
            time.sleep(5)

    log.error(f"All attempts failed. error: {last_exception}")
    raise last_exception


def get_auth_token(region, instance_id, user_name, cred):
    try:
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        http_profile = HttpProfile()
        http_profile.endpoint = "cam.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        request = GenerateAuthenticationTokenRequest(
            region=region,
            instance_id=instance_id,
            user_name=user_name,
            credential=cred,
            client_profile=client_profile,  # 可选
        )
        return DBAuthentication.generate_authentication_token(request)
    except TencentCloudSDKException as err:
        log.error(err)
        raise


if __name__ == "__main__":
    main()

```

### 错误码

参见 [错误码](https://cloud.tencent.com/document/product/598/33168)。

### 局限性

使用 CAM 数据库身份验证时存在一些限制。以下内容来自 CAM
身份验证文档。

当您使用 CAM 数据库身份验证时，您的应用程序必须生成 CAM 身份验证令牌。然后，您的应用程序使用该令牌连接到数据库实例或集群。

我们建议如下：

* 使用 CAM 数据库身份验证作为临时、个人访问数据库的机制。
* 仅对可以轻松重试的工作负载使用 CAM 数据库身份验证。