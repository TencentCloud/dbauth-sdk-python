import base64
import json
import logging
from datetime import datetime

from tencentcloud.cam.v20190116 import errorcodes
from tencentcloud.cam.v20190116.cam_client import CamClient
from tencentcloud.cam.v20190116.models import AuthToken
from tencentcloud.cam.v20190116.models import BuildDataFlowAuthTokenRequest
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from dbauth.internal.auth_token_parser import AuthTokenParser
from dbauth.internal.constants import Constants
from dbauth.internal.error_code_matcher import ErrorCodeMatcher
from dbauth.internal.timer_manager import TimerManager
from dbauth.internal.token import Token
from dbauth.internal.token_cache import TokenCache
from dbauth.internal.utils import Utils


class Signer:
    """Signer is a utility class that provides methods for generating and updating authentication tokens."""
    # The interval to update the token in milliseconds
    TOKEN_UPDATE_INTERVAL = 5 * 1000

    log = logging.getLogger(__name__)
    # The timer manager to schedule the token update
    timer_manager = TimerManager()
    # The token cache to store the authentication token
    token_cache = TokenCache()

    def __init__(self, request):
        # The request to generate the authentication token
        self.request = request
        key = (request.region + Constants.DELIMITER + request.instance_id + Constants.DELIMITER + request.user_name
               + Constants.DELIMITER + request.credential.secret_id)
        # The authentication key
        self.authKey = base64.b64encode(key.encode()).decode()

    def get_auth_token_from_cache(self):
        """Returns the authentication token from the cache."""
        return self.token_cache.get_auth_token(self.authKey)

    def build_auth_token(self):
        """Builds the authentication token."""
        self.log.debug("Building authentication token for key")
        try:
            # 1. Request the authentication token
            token = self.get_auth_token()
            dt = datetime.fromtimestamp(token.get_expires() / 1000.0)
            self.log.debug("Successfully get the authentication token, expiry: %s",
                           dt.strftime("%Y-%m-%d %H:%M:%S"))
            self.set_token_and_update_task(token)
        except TencentCloudSDKException as e:
            # 2. If the error code requires user notification, throw the exception
            if ErrorCodeMatcher.is_user_notification_required(e.code):
                raise e

            # 3. If the token generation fails, use the fallback token
            fallback_token = self.token_cache.fallback(self.request)
            if fallback_token:
                self.log.info("Using the fallback token")
                self.set_token_and_update_task(fallback_token)
            else:
                # 4. If there is no fallback token, throw the exception
                raise e

    def set_token_and_update_task(self, token):
        """Sets the authentication token and updates the token update task."""
        self.token_cache.set_auth_token(self.authKey, token)
        self.update_auth_token_task(token.get_expires())

    def get_auth_token(self):
        """Returns the authentication token."""
        response = self.request_auth_token()
        request_id = response.RequestId if response else ""  # Get the request ID
        if not response:
            self.log.error("Failed to request AuthToken, response is null")
            raise TencentCloudSDKException(errorcodes.INTERNALERROR,
                                           "Failed to request AuthToken, response is null",
                                           request_id)

        token_response = AuthToken()
        token_response.from_json_string(response.Credentials.to_json_string())
        if not token_response:
            self.log.error("Failed to request AuthToken, tokenResponse is null, request_id: %s", request_id)
            raise TencentCloudSDKException(errorcodes.INTERNALERROR,
                                           "Failed to request AuthToken, tokenResponse is null",
                                           request_id)

        # Decrypt the authToken
        enc_auth_token = token_response.Token
        try:
            auth_token = self.decrypt_auth_token(enc_auth_token)
        except Exception as e:
            error_message = "Failed to decrypt AuthToken, request_id: {}, error: {}".format(request_id, e)
            self.log.error(error_message)
            raise TencentCloudSDKException(errorcodes.INTERNALERROR, error_message, request_id)

        if not auth_token:
            self.log.error("Failed to decrypt AuthToken, authToken is empty, request_id: %s", request_id)
            raise TencentCloudSDKException(errorcodes.INTERNALERROR,
                                           "Failed to decrypt AuthToken, authToken is empty",
                                           request_id)

        cam_server_time = token_response.CurrentTime
        auth_token_expires = token_response.NextRotationTime

        # Calculate the expiry time of the authToken
        expiry = self.expiry(cam_server_time, auth_token_expires)
        return Token(auth_token, expiry)

    def decrypt_auth_token(self, enc_auth_token):
        """Decrypt the authentication token."""
        token_info = AuthTokenParser.parse_auth_token(self.request.instance_id, self.request.region,
                                                      self.request.user_name, enc_auth_token)
        return token_info.password

    def expiry(self, cam_server_time, auth_token_expires):
        """Calculate the expiry time of the authentication token."""
        if auth_token_expires < cam_server_time:
            return Utils.get_current_time_millis() + self.TOKEN_UPDATE_INTERVAL
        return Utils.get_current_time_millis() + (auth_token_expires - cam_server_time)

    def request_auth_token(self):
        """Requests an authentication token from the server."""
        req = BuildDataFlowAuthTokenRequest()
        params = {
            "ResourceId": self.request.instance_id,
            "ResourceRegion": self.request.region,
            "ResourceAccount": self.request.user_name
        }
        req.from_json_string(json.dumps(params))

        last_exception = None
        client = self.create_client()
        for _ in range(3):
            try:
                return client.BuildDataFlowAuthToken(req)
            except TencentCloudSDKException as e:
                last_exception = e
                if ErrorCodeMatcher.is_user_notification_required(e.code):
                    self.log.error("Failed to request AuthToken, error: %s", e)
                    break
                else:
                    self.log.error("Failed to request AuthToken, Retry to request the token,"
                                   " TencentCloudSDKException: %s", e)
            except Exception as e:
                self.log.error("Failed to request AuthToken, Retry to request the token, Exception: %s", e)
                last_exception = TencentCloudSDKException(errorcodes.INTERNALERROR,
                                                          "Failed to request AuthToken, error: {}".format(e),
                                                          "")

        raise last_exception

    def create_client(self):
        """Creates a new CAM client."""
        if self.request.client_profile:
            return CamClient(self.request.credential, self.request.region, self.request.client_profile)
        client = CamClient(self.request.credential, self.request.region)
        client.profile.httpProfile.reqTimeout = 30  # Set the request timeout to 30 seconds
        return client

    def update_auth_token_task(self, auth_token_expiry):
        """Updates the authentication token task."""
        # Calculate the remaining time before the token expires
        remaining_time_before_expiry = auth_token_expiry - Utils.get_current_time_millis()
        # Get the delay for the next token update
        delay_for_next_token_update = min(remaining_time_before_expiry, self.TOKEN_UPDATE_INTERVAL)

        self.log.debug("Scheduling next token key update in %s ms", delay_for_next_token_update)

        # Save the timer for the next token update
        self.timer_manager.save_timer(self.authKey, delay_for_next_token_update, self.auth_token_update_callback)

    def auth_token_update_callback(self):
        try:
            self.build_auth_token()
        except TencentCloudSDKException as e:
            if ErrorCodeMatcher.is_user_notification_required(e.code):
                # If a user notification is required, remove the token from the cache
                self.log.error("Failed to update the authentication token, error: %s", e)
                self.token_cache.remove_auth_token(self.authKey)
            else:
                # If an internal error occurs, try to update the token again
                self.log.error("Failed to update the authentication token, Retry to update the token, error: %s", e)
                self.update_auth_token_task(Utils.get_current_time_millis() + self.TOKEN_UPDATE_INTERVAL)
