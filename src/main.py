import os, shutil

def copy_static(source_path):
    if source_path == "public":
        if os.path.exists(source_path):
            shutil.rmtree(source_path)
            os.mkdir(source_path)
        else:
            os.mkdir(source_path)
        source_path = "static"

    dir_items = os.listdir(source_path)
    for item in dir_items:
        to_copy = os.path.join(source_path, item)
        target_path = to_copy.replace("static/", "")
        if not os.path.isfile(to_copy):
            new_dir = os.path.join("public", target_path)
            os.mkdir(new_dir)
            copy_static(to_copy)
        else:
            shutil.copy(to_copy, os.path.join("public", target_path))

def main():
    copy_static(source_path = "public")

main()