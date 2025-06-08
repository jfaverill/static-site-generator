import os, shutil

# function to copy contents from source directory to
# target directory
def copy_static(source_path, target_path):
    # if the target directory doesn't exist, then create it
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    # list the contents of the source directory
    source_items = os.listdir(source_path)
    # for each item in the listed contents...
    for item in source_items:
        # attach the item to the source path
        from_path = os.path.join(source_path, item)
        # attach the item to the target path
        to_path = os.path.join(target_path, item)
        # print what's being copied
        print(f" * {from_path} --> {to_path}")
        # if the source item is a directory, recursively call copy_static
        if not os.path.isfile(from_path):
            copy_static(from_path, to_path)
        # otherwise just copy the file to the target
        else:
            shutil.copy(from_path, to_path)

def main():

    source_path = "./static"
    target_path = "./public"

    # remove the target public directory and it's contents
    print(f"Deleting path \"{target_path}\"...")
    if os.path.exists(target_path):
        shutil.rmtree(target_path)

    # copy the contents from source static to target public
    print(f"Copying contents from \"{source_path}\" to \"{target_path}\"")
    copy_static(source_path, target_path)

main()