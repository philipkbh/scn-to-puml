import re


def parse_scn_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    content = content.replace("\n", "").replace("\t", "")

    node_pattern = re.compile(r"((?://.*?)+)?{(.*?)}", re.S)
    nodes = []

    for match in node_pattern.finditer(content):
        comments, node_data = match.groups()

        if comments:
            comments = comments.strip().split("//")
            comments = "\n".join(
                comment.strip() for comment in comments if comment
            )

        node_data = node_data.strip().split(";")
        node = {}
        for data in node_data:
            if data:
                key, value = data.split("=", 1)
                node[key.strip()] = value.strip()

        if comments:
            node["comment"] = comments

        nodes.append(node)

    return nodes


def generate_plantuml_script(nodes):
    plantuml_script = "@startuml class\n"
    plantuml_script += "hide circle\n\n"

    node_colors = {
        "object": "#FF9AA2",
        "shader": "#FFB7B2",
        "tex2d": "#FFDAC1",
        "texcube": "#E2F0CB",
        "separator": "#B5EAD7",
        "transform": "#C7CEEA",
        "geometry": "#9FD8DF",
        "camera": "#7EA6E0",
        "cave": "#B39BC8",
        "cave_camera": "#7D82B8",
        "window": "#A3D2CA",
        "light": "#D4E2D4",
        "skybox": "#A0C4FF",
        "renderstate": "#9CAFB7",
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
            if key not in ["type", "id", "parent"]:
                if key == "comment":
                    plantuml_script += f"  {{field}}{value}\n"
                else:
                    plantuml_script += f"  {{method}}{key}: {value}\n"
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
