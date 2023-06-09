# pyinstallerでパッケージ化後のファイル読み込み回りが煩雑になるので文字列で格納しておく
schemaV1 = """
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "SimutransImageMerger MergeDefinition Schema v1",
  "type": "object",
  "properties": {
    "version": {
      "type": "number",
      "enum": [
        1
      ]
    },
    "comment": {
      "type": "string"
    },
    "definitions": {
      "type": "array",
      "items": {
        "type": "object",
        "$ref": "#/definitions/definition"
      }
    }
  },
  "definitions": {
    "definition": {
      "type": "object",
      "properties": {
        "outputPath": {
          "type": "string"
        },
        "comment": {
          "type": "string"
        },
        "rules": {
          "type": "array",
          "items": {
            "oneOf": [
              {
                "$ref": "#/definitions/mergeImageRule"
              },
              {
                "$ref": "#/definitions/replaceColorRule"
              },
              {
                "$ref": "#/definitions/removeTransparentRule"
              },
              {
                "$ref": "#/definitions/removeSpecialColorRule"
              }
            ]
          }
        }
      },
      "required": [
        "outputPath",
        "rules"
      ]
    },
    "mergeImageRule": {
      "type": "object",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "type": "string",
          "enum": [
            "mergeImage"
          ]
        },
        "mode": {
          "type": "string",
          "enum": [
            "normal"
          ]
        },
        "pathes": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "offset": {
          "$ref": "#/definitions/offset"
        }
      },
      "required": [
        "name",
        "mode",
        "pathes",
        "offset"
      ]
    },
    "replaceColorRule": {
      "type": "object",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "type": "string",
          "enum": [
            "replaceColor"
          ]
        },
        "search": {
          "$ref": "#/definitions/rgb"
        },
        "replace": {
          "$ref": "#/definitions/rgba"
        }
      },
      "required": [
        "name",
        "search",
        "replace"
      ]
    },
    "removeTransparentRule": {
      "type": "object",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "type": "string",
          "enum": [
            "removeTransparent"
          ]
        },
        "threthold": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        }
      },
      "required": [
        "name",
        "threthold"
      ]
    },
    "removeSpecialColorRule": {
      "type": "object",
      "properties": {
        "comment": {
          "type": "string"
        },
        "name": {
          "type": "string",
          "enum": [
            "removeSpecialColor"
          ]
        }
      },
      "required": [
        "name"
      ]
    },
    "rgb": {
      "type": "object",
      "properties": {
        "r": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        },
        "g": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        },
        "b": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        }
      },
      "required": [
        "r",
        "g",
        "b"
      ]
    },
    "rgba": {
      "type": "object",
      "properties": {
        "r": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        },
        "g": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        },
        "b": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        },
        "a": {
          "type": "integer",
          "minimum": 0,
          "maximum": 255
        }
      },
      "required": [
        "r",
        "g",
        "b",
        "a"
      ]
    },
    "offset": {
      "type": "object",
      "properties": {
        "x": {
          "type": "integer"
        },
        "y": {
          "type": "integer"
        }
      },
      "required": [
        "x",
        "y"
      ]
    }
  },
  "required": [
    "version",
    "definitions"
  ]
}
"""
