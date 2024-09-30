import logging
import os
import unittest

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from dbauth.db_authentication import DBAuthentication
from dbauth.model.generate_authentication_token_request import GenerateAuthenticationTokenRequest

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(threadName)s] - {%(module)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class TestDBAuthentication(unittest.TestCase):
    log = logging.getLogger(__name__)

    def test_generate_authentication_token(self):
        ak, sk = os.environ['AK'], os.environ['SK']
        cred = credential.Credential(ak, sk)
        # Instantiate an HTTP option, optional, can be skipped if there are no special requirements
        httpProfile = HttpProfile(endpoint="cam.tencentcloudapi.com")
        # Instantiate a Client option, optional, can be skipped if there are no special requirements
        clientProfile = ClientProfile(httpProfile=httpProfile)

        request = GenerateAuthenticationTokenRequest(
            region="ap-guangzhou",
            instance_id="cdb-123456",
            user_name="camtest",
            credential=cred,
            client_profile=clientProfile  # option
        )
        result = DBAuthentication.generate_authentication_token(request)
        self.log.info(f"Generated authentication token: {result}")


if __name__ == '__main__':
    unittest.main()
