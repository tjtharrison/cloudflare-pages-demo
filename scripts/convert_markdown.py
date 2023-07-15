"""Script to generate HTML files from Markdown for publication."""
import glob
import os

import markdown

TEMPLATE_FILE = "template.html"


def get_files():
    """
    Get markdown files from the current directory.

    Raises:
        Exception: If unable to get markdown files.

    Returns:
            list: List of markdown files.
    """
    try:
        print("Getting a list of markdown files")
        all_markdown_files = list(glob.iglob("**/**.md", recursive=True))
    except Exception as error_message:
        print("Failed to get markdown files")
        raise Exception from error_message

    return all_markdown_files


def create_directories(all_markdown_files):
    """
    Process markdown files and create necessary subdirectories.

    Args:
        all_markdown_files (list): List of markdown files.

    Raises:
        Exception: If unable to create directories.

    Returns:
         True if successful
    """
    try:
        print("Creating directories")
        if not os.path.exists("docs"):
            print("Making directory docs")
            os.makedirs("docs")
        for file_name in all_markdown_files:
            if "/" in file_name:
                directory = "docs/" + file_name.rsplit("/", 1)[0]
                if not os.path.exists(directory):
                    print("Making directory " + directory)
                    os.makedirs(directory)
    except Exception as error_message:
        print("Failed to create directories")
        raise Exception from error_message

    return True

def convert_file(file_name):
    """
    Convert markdown file to HTML.

    Args:
        file_name (str): Name of markdown file.

    Raises:
        Exception: If unable to convert file.

    Returns:
        True if successful
    """
    try:
        print("Converting " + file_name + " to HTML")

        if file_name == "README.md":
            destination_file = "docs/index.html"
        else:
            destination_file = "docs/" + file_name.replace(".md", ".html")

        # Load Markdown content
        with open(file_name, "r+", encoding="UTF-8") as markdown_file:
            text = markdown_file.read()
            html = markdown.markdown(
                text,
                extensions=[
                    "attr_list",
                    "md_in_html",
                    "markdown.extensions.tables",
                    "pymdownx.superfences",
                ],
            )
            ## Formatting fixes
            fix_list = [
                ("./docs/", ""),
                ("<code>", "<pre>"),
                ("</code>", "</pre>"),
            ]
            for fix_item in fix_list:
                html = html.replace(fix_item[0], fix_item[1])

            # Append header block
            if "<!-- EndHead -->" in html:
                html = html.replace("<!-- EndHead -->", "</div></div>")
            else:
                html = "</div></div>" + html

            # Load header content
            with open(TEMPLATE_FILE, "r", encoding="UTF-8") as template_file:
                completed_template = template_file.read().replace("{{ BODY }}", html)

            # Build file
            with open(destination_file, "w", encoding="UTF-8") as html_file:
                html_file.write(completed_template)
            print(destination_file + " written!")
    except Exception as error_message:
        print("Failed to convert " + file_name + " to HTML: " + str(error_message))
        raise Exception from error_message

    return True

def main():
    """Launch main function."""
    # Get a list of markdown files
    try:
        all_markdown_files = get_files()
        print(all_markdown_files)
    except Exception as error_message:
        print("Failed to get markdown files")
        print(str(error_message))

    # Create necessary subdirectories
    try:
        create_directories(all_markdown_files)
    except Exception as error_message:
        print("Failed to create directories")
        print(str(error_message))

    # Convert each file
    for file_name in all_markdown_files:
        try:
            convert_file(file_name)
        except Exception as error_message:
            print("Failed to convert " + file_name)
            print(str(error_message))

    # Copy static directory into docs
    try:
        print("Copying static directory")
        os.system("cp -r static docs/")
    except Exception as error_message:
        print("Failed to copy static directory")
        print(str(error_message))


if __name__ == "__main__":
    main()
