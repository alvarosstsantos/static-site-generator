from os import listdir, makedirs, path
from shutil import copy, rmtree


def copy_static_content():
    pub_dir_path = path.join(".", "public")
    static_dir_path = path.join(".", "static")

    if (path.exists(pub_dir_path)):
        rmtree(pub_dir_path)

    makedirs(pub_dir_path)

    copy_tree(static_dir_path, pub_dir_path)


def copy_tree(source: str, destiny: str):
    for d in listdir(source):
        s = path.join(source, d)
        d = path.join(destiny, d)

        if path.isdir(s):
            makedirs(d)
            copy_tree(s, d)
        else:
            copy(s, d)


def main():
    copy_static_content()


if __name__ == "__main__":
    main()
