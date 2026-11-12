"""Schema validation of tool arguments, with a failure returned as a tool
execution error that the model can read and correct."""
import json

from jsonschema import Draft202012Validator

INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "report_id": {"type": "string", "pattern": "^[A-Z]{2}-[0-9]{4}$"}
    },
    "required": ["report_id"],
    "additionalProperties": False,
}
validator = Draft202012Validator(INPUT_SCHEMA)


def call_read_report(arguments):
    errors = [error.message for error in validator.iter_errors(arguments)]
    if errors:
        return {
            "resultType": "complete",
            "content": [{"type": "text", "text": "Invalid arguments: " + "; ".join(errors)}],
            "isError": True,
        }
    return {
        "resultType": "complete",
        "content": [{"type": "text", "text": f"Report {arguments['report_id']} loaded."}],
        "isError": False,
    }


if __name__ == "__main__":
    for arguments in ({"report_id": "FR-2031"}, {"report_id": "../../etc/passwd"}, {"report_id": "FR-2031", "debug": True}):
        print(json.dumps(arguments), "->", json.dumps(call_read_report(arguments)))
