from tencentcloud.cam.v20190116 import errorcodes
from tencentcloud.common import credential as Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException


class GenerateAuthenticationTokenRequest:
    def __init__(self, region: str, instance_id: str, user_name: str, credential: Credential, client_profile=None):
        if not region:
            raise TencentCloudSDKException(
                errorcodes.INVALIDPARAMETER_RESOURCEREGIONERROR, "The region is invalid."
            )
        if not instance_id:
            raise TencentCloudSDKException(
                errorcodes.INVALIDPARAMETER_RESOURCEERROR, "The instanceId is invalid."
            )
        if not user_name:
            raise TencentCloudSDKException(
                errorcodes.INVALIDPARAMETER_USERNAMEILLEGAL, "The userName is invalid."
            )
        if not credential or not credential.secretId or not credential.secretKey:
            raise TencentCloudSDKException(
                errorcodes.RESOURCENOTFOUND_SECRETNOTEXIST, "The credential is invalid."
            )

        self.region = region
        self.instance_id = instance_id
        self.user_name = user_name
        self.credential = credential
        self.client_profile = client_profile
