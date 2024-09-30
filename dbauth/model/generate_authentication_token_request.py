from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.cam.v20190116 import errorcodes
from tencentcloud.common import credential as Credential


class GenerateAuthenticationTokenRequest:
    def __init__(self, region: str, instance_id: str, user_name: str, credential: Credential, client_profile=None):
        if not region:
            raise TencentCloudSDKException(
                "The region is invalid.", "", errorcodes.INVALIDPARAMETER_RESOURCEREGIONERROR.value
            )
        if not instance_id:
            raise TencentCloudSDKException(
                "The instanceId is invalid.", "", errorcodes.INVALIDPARAMETER_RESOURCEERROR.value
            )
        if not user_name:
            raise TencentCloudSDKException(
                "The userName is invalid.", "", errorcodes.INVALIDPARAMETER_USERNAMEILLEGAL.value
            )
        if not credential or not credential.secretId or not credential.secretKey:
            raise TencentCloudSDKException(
                "The credential is invalid.", "", errorcodes.RESOURCENOTFOUND_SECRETNOTEXIST.value
            )

        self.region = region
        self.instance_id = instance_id
        self.user_name = user_name
        self.credential = credential
        self.client_profile = client_profile
