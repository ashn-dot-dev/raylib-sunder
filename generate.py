#!/usr/bin/env python3
from argparse import ArgumentParser
import json
import re

RE_TYPE_ARR = re.compile(r"(.*)\[(\d+)\]")
RE_TYPE_PTR = re.compile(r"(.*)\*")
RE_TYPE_UXX = re.compile(r"unsigned (.+)")

RE_DEFINE_COLOR = re.compile(r"CLITERAL\(Color\){ (\d+), (\d+), (\d+), (\d+) }")

def generate_type(s):
    s = s.replace("const", "").strip()
    match = RE_TYPE_ARR.match(s)
    if match:
        return f"[{match[2]}]{generate_type(match[1])}"
    match = RE_TYPE_PTR.match(s)
    if match:
        return f"*{generate_type(match[1])}"
    match = RE_TYPE_UXX.match(s)
    if match:
        return f"u{match[1]}"
    if s == "int":
        return "sint"
    if s == "short":
        return "sshort"
    if s == "long":
        return "slong"
    if s == "long long":
        return "long long"
    return s.strip()

def generate_version(j):
    name = j["name"]
    type = j["type"]
    value = j["value"]
    if name != "RAYLIB_VERSION":
        return None
    return f"let {name} = \"{value}\";"

def generate_color(j):
    name = j["name"]
    type = j["type"]
    value = j["value"]
    desc = j["description"]
    if type != "COLOR":
        return None
    match = RE_DEFINE_COLOR.match(value)
    return f"let {name} = (:Color){{.r={match[1]}, .g={match[2]}, .b={match[3]}, .a={match[4]}}}; # {desc}"
    return None


def generate_alias(j):
    name = j["name"]
    type = generate_type(j["type"])
    desc = j["description"]
    return f"alias {name} = {type}; # {desc}"

def generate_callback(j):
    is_variadic = False
    name = j["name"]
    desc = j["description"]
    func_params = list()
    for param in j["params"]:
        if param["type"] == "..." or param["type"] == "va_list":
            is_variadic = True
        param_type = generate_type(param["type"])
        func_params.append(param_type)
    func_return = generate_type(j["returnType"])
    if is_variadic:
        return "\n".join([
            f"# [SKIPPED] {name}: Callback of type `func({', '.join(func_params)}) {func_return}` is variadic.",
            f"alias {name} = *any; # {desc}"
        ])

    if len(desc) == 0:
        return f"alias {name} = func({', '.join(func_params)}) {func_return};"
    return f"alias {name} = func({', '.join(func_params)}) {func_return}; # {desc}"

def generate_enum(j):
    lines = list()
    name = j["name"]
    desc = j["description"]
    # XXX: Use uint override for config flags since SetConfigFlags takes
    # `unsigned int` as its `flags` parameter.
    type = "uint" if name == "ConfigFlags" else "sint"
    lines.append(f"alias {name} = {type}; # (enum) {desc}")
    for value in j["values"]:
        value_name = value["name"]
        value_value = value["value"]
        value_desc = value["description"]
        lines.append(f"let {value_name}: {name} = {value_value}; # {value_desc}")
    return "\n".join(lines)

def generate_struct(j):
    lines = list()
    name = j["name"]
    desc = j["description"]
    lines.append(f"struct {name} {{")
    for field in j["fields"]:
        field_name = field["name"]
        field_type = generate_type(field["type"])
        field_desc = field["description"]
        lines.append(f"    var {field_name}: {field_type}; # {field_desc}")
    lines.append(f"}}")
    return "\n".join(lines)

def generate_function(j):
    is_variadic = False
    name = j["name"]
    desc = j["description"]
    func_params = list()
    if "params" in j:
        for param in j["params"]:
            if param["type"] == "..." or param["type"] == "va_list":
                is_variadic = True
            param_name = param["name"]
            param_type = generate_type(param["type"])
            func_params.append(f"{param_name}: {param_type}")
    func_return = generate_type(j["returnType"])
    if is_variadic:
        return "\n".join([
            f"# [SKIPPED] {name}: Function of type `func({', '.join(func_params)}) {func_return}` is variadic.",
            f"alias {name} = *any; # {desc}"
        ])
    return f"extern func {name}({', '.join(func_params)}) {func_return}; # {desc}"

def main(args):
    with open(args.json) as f:
        api = json.loads(f.read())
    version = list(filter(lambda x: x is not None, map(generate_version, api["defines"])))
    colors = list(filter(lambda x: x is not None, map(generate_color, api["defines"])))
    aliases = list(map(generate_alias, api["aliases"]))
    # XXX: Opaque types discovered by a Sunder parse error.
    opaque = [
        "alias rAudioBuffer = any; # opaque struct",
        "alias rAudioProcessor = any; # opaque struct",
    ]
    callbacks = list(map(generate_callback, api["callbacks"]))
    enums = list(map(generate_enum, api["enums"]))
    structs = list(map(generate_struct, api["structs"]))
    functions = list(map(generate_function, api["functions"]))
    print("\n\n".join([
        "import \"c\";",
        "\n".join(version),
        "\n".join(colors),
        "\n".join(aliases),
        "\n".join(opaque),
        "\n".join(callbacks),
        "\n\n".join(enums),
        "\n\n".join(structs),
        "\n".join(functions),
    ]))

if __name__ == "__main__":
    parser = ArgumentParser(description="Generate bindings from the raylib API JSON")
    parser.add_argument("json")
    main(parser.parse_args())
