import json
import textwrap
from pathlib import Path

from openapi3 import OpenAPI
from openapi3.schemas import Schema


def indent(string):
    return textwrap.indent(string, "    ")


def wrap_comment(comment):
    return "\n".join(
        j
        for i in comment.splitlines()
        for j in textwrap.wrap(
            i,
            initial_indent="# ",
            subsequent_indent="# ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    )


ref_overrides = {
    "ch.datatrans.api.transactions.endpoint.status.StatusResponse$CardDetail": "StatusCardDetail",
    "ch.datatrans.api.transactions.endpoint.authorize.AuthorizeResponse$CardDetail": "AuthorizeCardDetail",
}


class Printer:
    def __init__(self):
        print("from typing import Any, List, Dict, TypedDict, Literal")

        self._printed_schemas = {}

    def _print_schema(self, schema: Schema):
        comment = schema.description or ""

        if schema.type == "object":
            if schema.properties is None:
                ref = "Dict[str, Any]"
            else:
                name = schema.path[-1]
                ref = ref_overrides.get(name, name.split(".")[-1].split("$")[-1])

                def field(field_name, field_schema):
                    r, c = self.get_schema_ref(field_schema)

                    if field_name in (schema.required or []):
                        c = f"{c}\n" f"Required."

                    return (
                        f"{wrap_comment(c)}\n" if c else ""
                    ) + f"{repr(field_name)}: {r}"

                fields_str = ",\n".join(
                    field(k, v) for k, v in schema.properties.items()
                )

                typeddict_args_str = (
                    f"{repr(ref)},\n"
                    f"{{\n"
                    f"{indent(fields_str)}}},\n"
                    f"total=False"
                )

                description = name

                if comment:
                    description = f"{description}\n{comment}"
                    comment = ""

                print(
                    f"\n"
                    f"\n"
                    f"{wrap_comment(description)}\n"
                    f"{ref} = TypedDict(\n"
                    f"{indent(typeddict_args_str)})"
                )
        elif schema.type == "array":
            r, c = self.get_schema_ref(schema.items)

            comment = comment or c
            ref = f"List[{r}]"
        elif schema.enum:
            literals_str = ", ".join(map(repr, schema.enum))

            ref = f"Literal[{literals_str}]"
        elif schema.type == "string":
            ref = "str"
        elif schema.type == "boolean":
            ref = "bool"
        elif schema.type == "integer":
            ref = "int"
        elif schema.type == "number":
            ref = "float"
        elif schema.type == "array":
            ref = "int"
        else:
            assert False, schema.type

        return ref, comment

    def get_schema_ref(self, schema: Schema) -> str:
        key = tuple(schema.path)
        ref = self._printed_schemas.get(key)

        if ref is None:
            self._printed_schemas[key] = ref = self._print_schema(schema)

        return ref


def generate(specification_file: Path):
    api = OpenAPI(json.loads(specification_file.read_bytes()))

    printer = Printer()

    for i in api.components.schemas.values():
        printer.get_schema_ref(i)
