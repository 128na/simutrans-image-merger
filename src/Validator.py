import json
from jsonschema import validate, exceptions
import sys
from src.schema import schemaV1


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
    version = data.get("version")
    if version == 1:
        return json.loads(schemaV1)

    raise Exception(f"invalid version provided: {version}")
