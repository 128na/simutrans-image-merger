import json
from typing import Final
from jsonschema import validate, exceptions
import os
import sys


def validateDefinition(jsonPath: str):
    data: dict = json.load(open(jsonPath, "r"))
    schema = getSchema(data)

    try:
        validate(data, schema)
        sys.stdout.write("validation passed")
        sys.exit(0)
    except exceptions.ValidationError as error:
        print(error)
        sys.exit(1)


def getSchema(data: dict):
    dirPath = os.path.dirname(os.path.realpath(__file__))
    version = data.get("version")
    if version == 1:
        schemaPath = os.path.join(dirPath, "schemas", "mergeDefinition_v1.json")
        return json.load(open(schemaPath, "r"))

    raise Exception(f"invalid version provided: {version}")
