from tencentcloud.cam.v20190116 import errorcodes


class ErrorCodeMatcher:
    ERROR_AUTH_FAILURE_PREFIX = "AuthFailure."

    @staticmethod
    def is_user_notification_required(error_code: str) -> bool:
        if not error_code:
            return False

        error_code_lower = error_code.lower()
        return (error_code_lower.startswith(ErrorCodeMatcher.ERROR_AUTH_FAILURE_PREFIX.lower()) or
                error_code_lower == errorcodes.RESOURCENOTFOUND_DATAFLOWAUTHCLOSE.lower())
