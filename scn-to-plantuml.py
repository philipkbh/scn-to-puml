import re


def parse_scn_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Remove newlines and tabs
    content = content.replace("\n", "").replace("\t", "")

    node_pattern = re.compile(r"{(.*?)}", re.S)
    nodes = []

    for match in node_pattern.finditer(content):
        node_data = match.group(1).strip().split(";")
        node = {}
        for data in node_data:
            if data:
                key, value = data.split("=", 1)
                node[key.strip()] = value.strip()

        nodes.append(node)

    return nodes


def generate_plantuml_script(nodes):
    plantuml_script = "@startuml class\n\n"

    node_colors = {
        "object": "#FFAAAA",
        "shader": "#AAFFAA",
        "tex2d": "#AAAAFF",
        "texcube": "#AAAAFF",
        "separator": "#FFAAFF",
        "transform": "#AACCFF",
        "geometry": "#FFCCAA",
        "camera": "#CCFFAA",
        "cave": "#CCFFAA",
        "cave_camera": "#CCFFAA",
        "window": "#CCAAFF",
        "light": "#FFFF00",
        "skybox": "#87CEEB",
        "renderstate": "#FFCCAA",
    }

    connection_attributes = [
        ("parent", "left"),
        ("texture", "right"),
        ("texture_env", "right"),
        ("shader", "right"),
        ("shader_tex", "right"),
        ("shader_color", "right"),
        ("shader_color_tex", "right"),
        ("shader_skybox", "right"),
        ("shader_env", "right"),
        ("window", "left"),
        ("cave", "right"),
        ("object", "right"),
    ]

    object_node_types = {}
    other_node_types = {}
    for node in nodes:
        if node["type"] == "object":
            object_node_types[node["id"]] = node["type"]
        else:
            other_node_types[node["id"]] = node["type"]

    for node in nodes:
        class_name = f"{node['type']}_{node['id']}"

        class_color = node_colors.get(node["type"], "#FFFFFF")

        plantuml_script += f"class {class_name} {class_color} {{\n"
        for key, value in node.items():
            if key not in ["id", "parent"]:
                plantuml_script += f"  {key}: {value}\n"
        plantuml_script += "}\n\n"

        for attr, position in connection_attributes:
            if attr in node:
                target_key = f"{node[attr]}"
                target_type = (
                    object_node_types[target_key]
                    if attr == "object"
                    else other_node_types[target_key]
                )
                target_class_name = f"{target_type}_{target_key}"

                if position == "left":
                    plantuml_script += f"{target_class_name} --> {class_name}\n"
                else:
                    plantuml_script += f"{class_name} --> {target_class_name}\n"

    plantuml_script += "@enduml"

    return plantuml_script


scn_file_path = "diablo_scene.scn"
nodes = parse_scn_file(scn_file_path)

plantuml_script = generate_plantuml_script(nodes)

with open("scene_graph.puml", "w") as file:
    file.write(plantuml_script)
