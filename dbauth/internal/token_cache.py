import os
import logging
from pathlib import Path
from dbauth.internal.constants import Constants
from dbauth.internal.utils import Utils
from dbauth.internal.token import Token


class TokenCache:
    MAX_PASSWORD_SIZE = 200

    def __init__(self):
        self.token_map = {}
        self.file_last_modify_time_map = {}
        self.log = logging.getLogger(__name__)

    def get_auth_token(self, key):
        return self.token_map.get(key)

    def set_auth_token(self, key, token):
        if key and token:
            self.token_map[key] = token

    def remove_auth_token(self, key):
        self.token_map.pop(key, None)

    def fallback(self, request):
        input_file_path = self.generate_input_file_path(request)
        if not input_file_path or not input_file_path.exists():
            return None

        try:
            file_size = input_file_path.stat().st_size
            self.log.info(f"File Name: {input_file_path}, File Size: {file_size}")

            if file_size == 0 or file_size > self.MAX_PASSWORD_SIZE:
                self.log.error(f"Invalid file size: {input_file_path}")
                return None

            lines = input_file_path.read_text().splitlines()
            if len(lines) == 0:
                return None
            if len(lines) > 1:
                self.log.error(f"The file has more than one line, skip the file: {input_file_path}")
                return None

            password = lines[0]
            if not password:
                return None

            self.log.info(f"Reading password: {input_file_path}")
            return Token(password, Utils.get_current_time_millis() + Constants.MAX_DELAY)

        except Exception as e:
            self.log.error(f"Failed to read password: {input_file_path}", exc_info=e)
            return None

    def generate_input_file_path(self, request):
        try:
            region, instance_id, user_name = request.region, request.instance_id, request.user_name
            path = Path(Constants.INPUT_PATH_DIR).joinpath(
                f"{region}{Constants.DELIMITER}{instance_id}{Constants.DELIMITER}{user_name}.pwd")
            return Path(os.getcwd()).joinpath(path)
        except Exception as e:
            self.log.error("Failed to decode key", exc_info=e)
            return None
