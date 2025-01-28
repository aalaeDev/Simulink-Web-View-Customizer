import glob
import json
import os
import xml.etree.ElementTree as ET

from utils.animate_svg_dashes import (
    add_animations,
    add_dashes,
    remove_animations,
    remove_dashes,
)


def modify_svg(svg_path, config):
    # Parse SVG file
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(svg_path)
    ns = {"svg": "http://www.w3.org/2000/svg"}
    root = tree.getroot()

    # Get config values from new structure
    svg_config = config["svg"]
    old_bg_color = svg_config["blocks"]["oldBackgroundColor"]
    bg_color = svg_config["blocks"]["backgroundColor"]
    old_fg_primary_color = svg_config["blocks"]["oldForegroundPrimaryColor"]
    fg_primary_color = svg_config["blocks"]["foregroundPrimaryColor"]
    old_fg_secondary_color = svg_config["blocks"]["oldForegroundSecondaryColor"]
    fg_secondary_color = svg_config["blocks"]["foregroundSecondaryColor"]
    use_images = svg_config["blocks"]["useImages"]
    use_gradients = svg_config["blocks"]["useGradients"]
    enable_background = svg_config["diagram"]["enableBackground"]
    font_family = svg_config["diagram"]["fontFamily"]
    use_dashed_lines = svg_config["connections"]["useDashedLines"]
    use_animations = svg_config["connections"]["useAnimations"]

    # Replace colors
    for elem in root.iter():
        # Replace fill colors
        if "fill" in elem.attrib:
            if elem.attrib["fill"] == old_bg_color:
                elem.attrib["fill"] = bg_color
            elif elem.attrib["fill"] == old_fg_primary_color:
                elem.attrib["fill"] = fg_primary_color
            elif elem.attrib["fill"] in old_fg_secondary_color:
                elem.attrib["fill"] = fg_secondary_color

        # Replace stroke colors
        if "stroke" in elem.attrib:
            if elem.attrib["stroke"] == old_fg_primary_color:
                elem.attrib["stroke"] = fg_primary_color
            elif elem.attrib["stroke"] in old_fg_secondary_color:
                elem.attrib["stroke"] = fg_secondary_color

        # Replace font-family
        if "font-family" in elem.attrib:
            elem.attrib["font-family"] = font_family

    # Remove images if not using them
    if not use_images:
        for parent in root.findall(".//*"):
            for image in parent.findall("svg:image", ns):
                parent.remove(image)

    # Remove gradients if not using them
    if not use_gradients:
        # Remove gradient definitions
        for defs in root.findall(".//*svg:defs", ns):
            for grad in defs.findall("svg:linearGradient", ns):
                defs.remove(grad)

        # Remove gradient references
        for elem in root.iter():
            if "fill" in elem.attrib and elem.attrib["fill"].startswith("url(#grad"):
                elem.attrib["fill"] = bg_color

    # Handle background based on enable_background setting
    if not enable_background:
        for parent in root.findall(".//*"):
            for bg in parent.findall("*[@id='background']"):
                parent.remove(bg)

    # Toggle dashed lines
    if use_dashed_lines:
        add_dashes(root)
    else:
        remove_dashes(root)

    # Toggle flow animations
    if use_animations:
        add_animations(root)
    else:
        remove_animations(root)

    # Save modified SVG
    tree.write(svg_path, encoding="utf-8", xml_declaration=True)


def update_config_colors(config):
    svg_config = config["svg"]["blocks"]

    # Update old colors to match current colors
    svg_config["oldBackgroundColor"] = svg_config["backgroundColor"]
    svg_config["oldForegroundPrimaryColor"] = svg_config["foregroundPrimaryColor"]
    svg_config["oldForegroundSecondaryColor"] = svg_config["foregroundSecondaryColor"]

    # Update Config
    config["svg"]["blocks"] = svg_config

    # Write updated config back to file
    with open("ui.config.json", "w") as f:
        json.dump(config, f, indent=4)


def process_all_svgs(config):
    svg_dir = config["svg"]["path"]

    # Find all SVG files in the directory
    svg_pattern = os.path.join(svg_dir, "*.svg")
    svg_files = glob.glob(svg_pattern)

    # Process each SVG file
    for svg_file in svg_files:
        print(f"Processing {svg_file}...")
        modify_svg(svg_file, config)

    # Update the config file with new colors
    update_config_colors(config)
