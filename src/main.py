from os import listdir, makedirs, path
import re
from shutil import copy, rmtree

from parser import markdown_to_html_node


def copy_static_content():
    pub_dir_path = path.join(".", "public")
    static_dir_path = path.join(".", "static")

    if (path.exists(pub_dir_path)):
        rmtree(pub_dir_path)

    makedirs(pub_dir_path)

    copy_tree(static_dir_path, pub_dir_path)

    from_path = path.join(".", "content")
    template_path = path.join(".", "template.html")
    dest_path = path.join(pub_dir_path)

    generate_pages_recursive(from_path, template_path, dest_path)


def copy_tree(source: str, destiny: str):
    for d in listdir(source):
        s = path.join(source, d)
        d = path.join(destiny, d)

        if path.isdir(s):
            makedirs(d)
            copy_tree(s, d)
        else:
            copy(s, d)


def extract_title(markdown: str):
    match = re.findall(r"^# .+", markdown)

    if len(match) > 0:
        return match[0][2:].strip()

    raise ValueError("No H1 Heading found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for d in listdir(dir_path_content):
        s = path.join(dir_path_content, d)
        d = path.join(dest_dir_path, d)

        if path.isdir(s):
            makedirs(d)
            generate_pages_recursive(s, template_path, d)
        else:
            d = d[:-2]+"html"
            print(f"Generating page from {s} to {
                d} using {template_path}")

            template_file = open(template_path, 'r')
            template = template_file.read()
            template_file.close()

            content_file = open(path.join(s), 'r')
            content_md = content_file.read()
            content_file.close()

            content = markdown_to_html_node(content_md).to_html()
            title = extract_title(content_md)

            index_html = template.replace(
                "{{ Title }}", title).replace("{{ Content }}", content)

            with open(d, 'w') as f:
                f.write(index_html)


def main():
    copy_static_content()


if __name__ == "__main__":
    main()
