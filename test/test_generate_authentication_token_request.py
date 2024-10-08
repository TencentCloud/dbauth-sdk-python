import unittest

from tencentcloud.cam.v20190116 import errorcodes
from tencentcloud.common import credential as Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from dbauth.model.generate_authentication_token_request import GenerateAuthenticationTokenRequest


class TestGenerateAuthenticationTokenRequest(unittest.TestCase):

    def test_valid_request_initialization(self):
        cred = Credential.Credential("secretId", "secretKey")
        request = GenerateAuthenticationTokenRequest("ap-guangzhou", "instance123", "user123", cred)
        self.assertEqual(request.region, "ap-guangzhou")
        self.assertEqual(request.instance_id, "instance123")
        self.assertEqual(request.user_name, "user123")
        self.assertEqual(request.credential, cred)

    def test_invalid_region_raises_exception(self):
        cred = Credential.Credential("secretId", "secretKey")
        with self.assertRaises(TencentCloudSDKException) as context:
            GenerateAuthenticationTokenRequest("", "instance123", "user123", cred)
        self.assertEqual(context.exception.get_code(), errorcodes.INVALIDPARAMETER_RESOURCEREGIONERROR)

    def test_invalid_instance_id_raises_exception(self):
        cred = Credential.Credential("secretId", "secretKey")
        with self.assertRaises(TencentCloudSDKException) as context:
            GenerateAuthenticationTokenRequest("ap-guangzhou", "", "user123", cred)
        self.assertEqual(context.exception.get_code(), errorcodes.INVALIDPARAMETER_RESOURCEERROR)

    def test_invalid_user_name_raises_exception(self):
        cred = Credential.Credential("secretId", "secretKey")
        with self.assertRaises(TencentCloudSDKException) as context:
            GenerateAuthenticationTokenRequest("ap-guangzhou", "instance123", "", cred)
        self.assertEqual(context.exception.get_code(), errorcodes.INVALIDPARAMETER_USERNAMEILLEGAL)

    def test_invalid_credential_raises_exception(self):
        with self.assertRaises(TencentCloudSDKException) as context:
            GenerateAuthenticationTokenRequest("ap-guangzhou", "instance123", "user123", None)
        self.assertEqual(context.exception.get_code(), errorcodes.RESOURCENOTFOUND_SECRETNOTEXIST)


if __name__ == '__main__':
    unittest.main()
