# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: auth_token_info.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61uth_token_info.proto\x12\x0c\x64\x62\x61uth.proto\"\xdf\x01\n\rAuthTokenInfo\x12\r\n\x05\x61ppId\x18\x01 \x01(\x04\x12\x0b\n\x03uin\x18\x02 \x01(\x04\x12\x10\n\x08ownerUin\x18\x03 \x01(\x04\x12\r\n\x05reqId\x18\x04 \x01(\t\x12\x12\n\ninstanceId\x18\x05 \x01(\t\x12\x0e\n\x06region\x18\x06 \x01(\t\x12\x10\n\x08username\x18\x07 \x01(\t\x12\x10\n\x08password\x18\x08 \x01(\t\x12\x12\n\ncreateTime\x18\t \x01(\x04\x12\x11\n\textraInfo\x18\n \x01(\t\x12\x11\n\ttokenType\x18\x0b \x01(\r\x12\x0f\n\x07randNum\x18\x0c \x01(\rb\x06proto3')



_AUTHTOKENINFO = DESCRIPTOR.message_types_by_name['AuthTokenInfo']
AuthTokenInfo = _reflection.GeneratedProtocolMessageType('AuthTokenInfo', (_message.Message,), {
  'DESCRIPTOR' : _AUTHTOKENINFO,
  '__module__' : 'auth_token_info_pb2'
  # @@protoc_insertion_point(class_scope:dbauth.proto.AuthTokenInfo)
})
_sym_db.RegisterMessage(AuthTokenInfo)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AUTHTOKENINFO._serialized_start=40
  _AUTHTOKENINFO._serialized_end=263
# @@protoc_insertion_point(module_scope)
