import os, shutil

def copy_static(source_path, target_path):
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    source_items = os.listdir(source_path)
    for item in source_items:
        from_path = os.path.join(source_path, item)
        to_path = os.path.join(target_path, item)
        print(f" * {from_path} --> {to_path}")
        if not os.path.isfile(from_path):
            copy_static(from_path, to_path)
        else:
            shutil.copy(from_path, to_path)

def main():

    source_path = "./static"
    target_path = "./public"

    # remove the target public directory and it's contents
    print(f"Deleting path \"{target_path}\"...")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    print(f"Copying contents from \"{source_path}\" to \"{target_path}\"")
    copy_static(source_path, target_path)

main()