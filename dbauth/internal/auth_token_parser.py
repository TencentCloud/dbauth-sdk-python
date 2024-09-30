import hashlib
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from google.protobuf.message import DecodeError
import dbauth.proto.auth_token_info_pb2 as proto
from dbauth.internal.constants import Constants


class AuthTokenParser:
    class AuthTokenParserError(Exception):
        pass

    @staticmethod
    def parse_auth_token(instance_id: str, region: str, user_name: str, token: str) -> proto.AuthTokenInfo:
        if not all([instance_id, region, user_name, token]):
            raise AuthTokenParser.AuthTokenParserError("param empty")

        seed_key = AuthTokenParser._sha256(
            f"{instance_id}{Constants.DELIMITER}{region}{Constants.DELIMITER}{user_name}".encode())
        key, iv = seed_key[:32], seed_key[33:49]

        decrypted_token = AuthTokenParser._decrypt(token[64:], key, iv)
        if token[:64] != AuthTokenParser._sha256(decrypted_token):
            raise AuthTokenParser.AuthTokenParserError("token not compare")

        return AuthTokenParser._get_auth_token_info(decrypted_token)

    @staticmethod
    def _get_auth_token_info(decrypted_token: bytes) -> proto.AuthTokenInfo:
        try:
            auth_token_info = proto.AuthTokenInfo()
            auth_token_info.ParseFromString(decrypted_token[4:])
            return auth_token_info
        except DecodeError as e:
            raise AuthTokenParser.AuthTokenParserError("Failed to parse AuthTokenInfo") from e

    @staticmethod
    def _sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    @staticmethod
    def _decrypt(encrypted_data: str, key: str, iv: str) -> bytes:
        cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
        decrypted_padded_plaintext = cipher.decrypt(AuthTokenParser._base64_decode(encrypted_data))
        return unpad(decrypted_padded_plaintext, AES.block_size)

    @staticmethod
    def _base64_decode(data: str) -> bytes:
        data = data.replace("-", "+").replace("_", "/")

        mod4 = len(data) % 4
        if mod4 != 0:
            data += "===="[:4 - mod4]

        return base64.b64decode(data)
