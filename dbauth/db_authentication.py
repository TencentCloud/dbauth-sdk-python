import logging
from dbauth.internal.utils import Utils
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from .internal.error_code_matcher import ErrorCodeMatcher
from .internal.signer import Signer
from .model.generate_authentication_token_request import GenerateAuthenticationTokenRequest


class DBAuthentication:
    """DBAuthentication is a utility class that provides methods for generating authentication tokens."""
    log = logging.getLogger(__name__)

    @staticmethod
    def generate_authentication_token(token_request: GenerateAuthenticationTokenRequest) -> str:
        """Generates an authentication token using the provided request."""
        # Create a new Signer with the provided token request.
        signer = Signer(token_request)
        # Get the authentication token from the cache.
        cached_token = signer.get_auth_token_from_cache()
        if cached_token:
            if cached_token.get_expires() > Utils.get_current_time_millis():
                # If the token has not expired, return the token.
                return cached_token.get_auth_token()
        try:
            signer.build_auth_token()
            return signer.get_auth_token_from_cache().get_auth_token()
        except TencentCloudSDKException as e:
            DBAuthentication.log.error("Error occurred while generating authentication token", exc_info=e)
            if cached_token:
                if ErrorCodeMatcher.is_user_notification_required(e.code):
                    raise e
                else:
                    return cached_token.get_auth_token()
            raise e
