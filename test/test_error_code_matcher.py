import unittest

from tencentcloud.cam.v20190116 import errorcodes

from dbauth.internal.error_code_matcher import ErrorCodeMatcher


class TestErrorCodeMatcher(unittest.TestCase):

    def test_is_user_notification_required_valid_error_code(self):
        error_code = "AuthFailure.InvalidSecretId"
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_valid_error_code_lower(self):
        error_code = "AuthFailure.InvalidSecretId".lower()
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_valid_error_code_upper(self):
        error_code = "AuthFailure.InvalidSecretId".upper()
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_resource_not_found(self):
        error_code = errorcodes.RESOURCENOTFOUND_DATAFLOWAUTHCLOSE
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_resource_not_found_lower(self):
        error_code = errorcodes.RESOURCENOTFOUND_DATAFLOWAUTHCLOSE.lower()
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_resource_not_found_upper(self):
        error_code = errorcodes.RESOURCENOTFOUND_DATAFLOWAUTHCLOSE.upper()
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertTrue(result)

    def test_is_user_notification_required_invalid_error_code(self):
        error_code = "InvalidParameter"
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertFalse(result)

    def test_is_user_notification_required_resource_not_found_exception(self):
        error_code = errorcodes.RESOURCENOTFOUND_DATAFLOWAUTHCLOSE + "Exception"
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertFalse(result)

    def test_is_user_notification_required_empty_error_code(self):
        error_code = ""
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertFalse(result)

    def test_is_user_notification_required_none_error_code(self):
        error_code = None
        result = ErrorCodeMatcher.is_user_notification_required(error_code)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
