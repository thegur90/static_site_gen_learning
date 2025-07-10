import os
import shutil
from block_markdown import extract_title,markdown_to_html_node

r"""


Full disclosure: As far as "copy static" goes - I intend to "cheat" this part of the lesson using rmtree and copytree.
I'm using a system that is otherwise used in production for my learning experience, I will use every safety measure i can think of to not accidentally delete or move the wrong file.
I can iterate through a filetree in a function that won't also delete it. list_all_filepaths_in_folder(folder) exists to prove that point :)
Backend developers have to be extra careful about file safety even when they can't think straight, and this course took my brain and chucked it into a centrifuge.


"""
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(SCRIPT_DIR)
CONTENT_DIR = os.path.join(MAIN_DIR,"content")

def delete_public_directory():
    path = os.path.join(MAIN_DIR,"public")
    if os.path.exists(path):
        shutil.rmtree(path)

def copy_static_to_public():
    static = os.path.join(MAIN_DIR,"static")
    public = os.path.join(MAIN_DIR,"public")
    shutil.copytree(static,public)

def list_all_filepaths_in_folder(folder):
    returned_list = []
    for item in os.listdir(folder):
        entry = os.path.join(folder,item)
        if os.path.isdir(entry):
            returned_list.extend(list_all_filepaths_in_folder(entry))
        elif os.path.isfile(entry):
            returned_list.append(entry)
    return returned_list

def list_all_md_files_in_dir(dir):
    returned = []
    for entry in list_all_filepaths_in_folder(dir):
        if entry.endswith(".md"):
            returned.append(entry)
    return returned


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    old_filepaths = list_all_md_files_in_dir(dir_path_content)

    for md_path in old_filepaths:
        rel_path = os.path.relpath(md_path, CONTENT_DIR)
        html_rel_path = rel_path[:-3] + ".html"
        dest_path = os.path.join(dest_dir_path, html_rel_path)
        print(f"md_path={md_path}")
        print("\n")
        print(f"rel_path={rel_path}")
        print("\n")
        print(f"html_rel_path={html_rel_path}")
        print("\n")
        print(f"dest_path={dest_path}")
        print("\n")
        generate_page(md_path, template_path, dest_path)
    

def generate_page(from_path, template_path, dest_path):
    #init
    source_html_title = ""
    source_html_content = ""
    template = ""
    print (f"Generating page from {from_path} to {dest_path} using {template_path}...")

    with open(from_path, 'r') as m:
        m_string = m.read()
        source_html_title = extract_title(m_string)
        source_html_content = markdown_to_html_node(m_string).to_html()

    with open(template_path, 'r') as n:
        template = n.read()

    template = template.replace("{{ Title }}", source_html_title)
    template = template.replace("{{ Content }}", source_html_content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, 'w') as output:
        output.write(template)
    

def main():
    delete_public_directory()
    copy_static_to_public()
    generate_pages_recursive(os.path.join(MAIN_DIR,"content"),os.path.join(MAIN_DIR,"template.html"),os.path.join(MAIN_DIR,"public"))

if __name__ == "__main__":
    main()
