def extract_title(markdown):
    title = None
    markdown_lines = markdown.split("\n")
    for line in markdown_lines:
        if line[:2] == "# ":
            title = line[2:]
            break
    if title is None:
        raise Exception("No h1 header in markdown")
    return title