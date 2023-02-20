from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ColValue(_message.Message):
    __slots__ = ["column_name", "column_value"]
    COLUMN_NAME_FIELD_NUMBER: _ClassVar[int]
    COLUMN_VALUE_FIELD_NUMBER: _ClassVar[int]
    column_name: str
    column_value: str
    def __init__(self, column_name: _Optional[str] = ..., column_value: _Optional[str] = ...) -> None: ...

class DeleteRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class DeleteResponse(_message.Message):
    __slots__ = ["affected_rows", "error"]
    AFFECTED_ROWS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    affected_rows: int
    error: Issue
    def __init__(self, affected_rows: _Optional[int] = ..., error: _Optional[_Union[Issue, _Mapping]] = ...) -> None: ...

class GetRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class GetResponse(_message.Message):
    __slots__ = ["error", "rows"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    error: Issue
    rows: _containers.RepeatedCompositeFieldContainer[Rows]
    def __init__(self, rows: _Optional[_Iterable[_Union[Rows, _Mapping]]] = ..., error: _Optional[_Union[Issue, _Mapping]] = ...) -> None: ...

class InsertRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class InsertResponse(_message.Message):
    __slots__ = ["error", "insert_id"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    INSERT_ID_FIELD_NUMBER: _ClassVar[int]
    error: Issue
    insert_id: int
    def __init__(self, insert_id: _Optional[int] = ..., error: _Optional[_Union[Issue, _Mapping]] = ...) -> None: ...

class Issue(_message.Message):
    __slots__ = ["error_code", "error_message"]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    error_code: int
    error_message: str
    def __init__(self, error_code: _Optional[int] = ..., error_message: _Optional[str] = ...) -> None: ...

class Rows(_message.Message):
    __slots__ = ["values"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[ColValue]
    def __init__(self, values: _Optional[_Iterable[_Union[ColValue, _Mapping]]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["query"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    query: str
    def __init__(self, query: _Optional[str] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["affected_rows", "error"]
    AFFECTED_ROWS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    affected_rows: int
    error: Issue
    def __init__(self, affected_rows: _Optional[int] = ..., error: _Optional[_Union[Issue, _Mapping]] = ...) -> None: ...
