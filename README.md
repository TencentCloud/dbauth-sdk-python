Language : 🇺🇸 | [🇨🇳](./README.zh-CN.md)
<h1 align="center">Tencent Cloud DBAuth SDK</h1>
<div align="center">
Welcome to the Tencent Cloud DBAuth SDK, which provides developers with supporting development tools to access the Tencent Cloud Database CAM verification service, simplifying the access process of the Tencent Cloud Database CAM verification service.
</div>

### Dependency Environment

1. Dependency Environment: Python 3.6 and above.
2. Before use, CAM verification must be enabled on the Tencent Cloud console.
3. On the Tencent Cloud console, view the account APPID on
   the [account information](https://console.cloud.tencent.com/developer) page, and obtain the SecretID and SecretKey on
   the [access management](https://console.cloud.tencent.com/cam/capi) page.

### Install via pip

You can install the Tencent Cloud Database CAM Python SDK into your project using pip.
Please execute the following command in your command line:

```bash
pip install git+https://github.com/TencentCloud/dbauth-sdk-python.git
```

Please note that if you have both Python 2 and Python 3 environments, you need to use the pip3 command to install it in
the Python 3 environment.

#### Indirect Dependencies

For tencentcloud-sdk-python version 3.0.1224 and above.

### Example - Connect to a Database Instance

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

# Configure root logger
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
        # Get the connection
        connection = get_db_connection_using_cam(secret_id, secret_key, region,
                                                 instance_id, user_name, host, port, db_name)

        # Verify the connection is successful
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'Success!';")
            result = cursor.fetchone()
            log.info(result[0])  # Should print "Success!"
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
        # Instantiate an HTTP option, optional, can be skipped if there are no special requirements
        http_profile = HttpProfile()
        http_profile.endpoint = "cam.tencentcloudapi.com"

        # Instantiate a Client option, optional, can be skipped if there are no special requirements
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        request = GenerateAuthenticationTokenRequest(
            region=region,
            instance_id=instance_id,
            user_name=user_name,
            credential=cred,
            client_profile=client_profile,  # optional
        )
        return DBAuthentication.generate_authentication_token(request)
    except TencentCloudSDKException as err:
        log.error(err)
        raise


if __name__ == "__main__":
    main()

```

### Error Codes

Refer to the [error code document](https://cloud.tencent.com/document/product/598/33168) for more information.

### Limitations

There are some limitations when you use CAM database authentication. The following is from the CAM authentication
documentation.

When you use CAM database authentication, your application must generate an CAM authentication token. Your application
then uses that token to connect to the DB instance or cluster.

We recommend the following:

* Use CAM database authentication as a mechanism for temporary, personal access to databases.
* Use CAM database authentication only for workloads that can be easily retried.