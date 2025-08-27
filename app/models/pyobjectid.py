# app/models/pyobjectid.py
from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid objectid: {v}")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: JsonSchemaValue, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        # ObjectId는 문자열로 직렬화되므로 string 타입으로 지정
        return {
            "type": "string",
            "examples": ["60dbf3b4f9c9b91320d5c5e4"],
            "description": "MongoDB ObjectId 형식 문자열"
        }
