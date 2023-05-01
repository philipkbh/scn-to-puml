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
    plantuml_script = "@startuml class\n\n"

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

        if "parent" in node:
            parent_key = f"{node['parent']}"
            parent_type = other_node_types[parent_key]
            parent_class_name = f"{parent_type}_{parent_key}"
            plantuml_script += f"{parent_class_name} --> {class_name}\n"

        if "texture" in node:
            texture_key = f"{node['texture']}"
            texture_type = other_node_types[texture_key]
            texture_class_name = f"{texture_type}_{texture_key}"
            plantuml_script += f"{class_name} --> {texture_class_name}\n"

        if "texture_env" in node:
            texture_env_key = f"{node['texture_env']}"
            texture_env_type = other_node_types[texture_env_key]
            texture_env_class_name = f"{texture_env_type}_{texture_env_key}"
            plantuml_script += f"{class_name} --> {texture_env_class_name}\n"

        if "shader" in node:
            shader_key = f"{node['shader']}"
            shader_type = other_node_types[shader_key]
            shader_class_name = f"{shader_type}_{shader_key}"
            plantuml_script += f"{class_name} --> {shader_class_name}\n"

        if "shader_tex" in node:
            shader_tex_key = f"{node['shader_tex']}"
            shader_tex_type = other_node_types[shader_tex_key]
            shader_tex_class_name = f"{shader_tex_type}_{shader_tex_key}"
            plantuml_script += f"{class_name} --> {shader_tex_class_name}\n"

        if "shader_color" in node:
            shader_color_key = f"{node['shader_color']}"
            shader_color_type = other_node_types[shader_color_key]
            shader_color_class_name = f"{shader_color_type}_{shader_color_key}"
            plantuml_script += f"{class_name} --> {shader_color_class_name}\n"

        if "shader_color_tex" in node:
            shader_color_tex_key = f"{node['shader_color_tex']}"
            shader_color_tex_type = other_node_types[shader_color_tex_key]
            shader_color_tex_class_name = (
                f"{shader_color_tex_type}_{shader_color_tex_key}"
            )
            plantuml_script += (
                f"{class_name} --> {shader_color_tex_class_name}\n"
            )

        if "shader_skybox" in node:
            shader_skybox_key = f"{node['shader_skybox']}"
            shader_skybox_type = other_node_types[shader_skybox_key]
            shader_skybox_class_name = (
                f"{shader_skybox_type}_{shader_skybox_key}"
            )
            plantuml_script += f"{class_name} --> {shader_skybox_class_name}\n"

        if "shader_env" in node:
            shader_env_key = f"{node['shader_env']}"
            shader_env_type = other_node_types[shader_env_key]
            shader_env_class_name = f"{shader_env_type}_{shader_env_key}"
            plantuml_script += f"{class_name} --> {shader_env_class_name}\n"

        if "window" in node:
            window_key = f"{node['window']}"
            window_type = other_node_types[window_key]
            window_class_name = f"{window_type}_{window_key}"
            plantuml_script += f"{window_class_name} --> {class_name}\n"

        if "cave" in node:
            cave_key = f"{node['cave']}"
            cave_type = other_node_types[cave_key]
            cave_class_name = f"{cave_type}_{cave_key}"
            plantuml_script += f"{class_name} --> {cave_class_name}\n"

        if "object" in node:
            object_key = f"{node['object']}"
            object_type = object_node_types[object_key]
            object_class_name = f"{object_type}_{object_key}"
            plantuml_script += f"{class_name} --> {object_class_name}\n"

    plantuml_script += "@enduml"

    return plantuml_script


scn_file_path = "diablo_scene.scn"
nodes = parse_scn_file(scn_file_path)

plantuml_script = generate_plantuml_script(nodes)

with open("scene_graph.puml", "w") as file:
    file.write(plantuml_script)
