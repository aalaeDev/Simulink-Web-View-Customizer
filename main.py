from utils import load_config
from utils.modify_html import modify_html
from utils.modify_svg import process_all_svgs
from utils.modify_thumbnails import modify_thumbnails


def main():
    config = load_config("ui.config.json")
    process_all_svgs(config)
    modify_html(config)
    modify_thumbnails(config["svg"]["path"])


if __name__ == "__main__":
    main()
