import xml.etree.ElementTree as ET


def add_dashes(root):
    # Find all groups with PathIntersectionsEnabledTag
    for tagged_group in root.findall(".//*[@data-tags='PathIntersectionsEnabledTag']"):
        # Find paths within these groups that are part of line segments
        # The paths are directly under the g elements
        for path in tagged_group.findall("./*/*/*[@d]"):
            # Skip arrowhead paths (which are triangular markers)
            if not path.get("d", "").startswith("M0,0") and "z" not in path.get(
                "d", ""
            ):
                # Add stroke-dasharray if not present
                if not path.get("stroke-dasharray"):
                    path.set("stroke-dasharray", "4,4")


def remove_dashes(root):
    # Find all groups with PathIntersectionsEnabledTag
    for tagged_group in root.findall(".//*[@data-tags='PathIntersectionsEnabledTag']"):
        # Find paths within these groups
        for path in tagged_group.findall("./*/*/*[@d]"):
            if "stroke-dasharray" in path.attrib:
                path.attrib.pop("stroke-dasharray")


def add_animations(root):
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Add animation styles if not present
    has_animations = any(
        "keyframes dash" in style.text for style in root.findall(".//svg:style", ns)
    )
    if not has_animations:
        style_element = ET.Element("style")
        style_element.text = """
            @keyframes dash {
                to {
                    stroke-dashoffset: -16;
                }
            }
            .animated-dash {
                animation: dash 1s linear infinite;
            }
        """
        root.insert(1, style_element)

    # Add animation classes to paths
    for tagged_group in root.findall(".//*[@data-tags='PathIntersectionsEnabledTag']"):
        for path in tagged_group.findall("./*/*/*[@d]"):

            # Skip arrowhead paths
            if not path.get("d", "").startswith("M0,0") and "z" not in path.get(
                "d", ""
            ):
                classes = path.get("class", "").split()
                if "animated-dash" not in classes:
                    classes.append("animated-dash")
                    path.set("class", " ".join(classes))


def remove_animations(root):
    # Remove animation styles
    ns = {"svg": "http://www.w3.org/2000/svg"}
    for style in root.findall(".//svg:style", ns):
        if "keyframes dash" in style.text:
            root.remove(style)

    # Remove animation classes from paths
    for tagged_group in root.findall(".//*[@data-tags='PathIntersectionsEnabledTag']"):
        for path in tagged_group.findall("./*/*/*[@d]"):
            classes = path.get("class", "").split()
            if "animated-dash" in classes:
                classes.remove("animated-dash")
                if classes:
                    path.set("class", " ".join(classes))
                else:
                    path.attrib.pop("class", None)
