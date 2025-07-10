import os
import shutil
from block_markdown import extract_title,markdown_to_html_node

r"""


Full disclosure: As far as "copy static" goes - I intend to "cheat" this part of the lesson using rmtree and copytree.
I'm using a system that is otherwise used in production for my learning experience, I will use every safety measure i can think of to not accidentally delete or move the wrong file.
I can iterate through a filetree for fun later in a function that won't also delete it. (and I might actually do that very soon in a personal project :P )

But yea. i'll save the fun part for when i feel more comfortable about not breaking my filesystem.
Backend developers have to be extra careful about file safety even when they can't think straight!


"""
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(SCRIPT_DIR)

def delete_public_directory():
    path = os.path.join(MAIN_DIR,"public")
    if os.path.exists(path):
        shutil.rmtree(path)

def copy_static_to_public():
    static = os.path.join(MAIN_DIR,"static")
    public = os.path.join(MAIN_DIR,"public")
    shutil.copytree(static,public)

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
    generate_page(os.path.join(MAIN_DIR,"content","index.md"),os.path.join(MAIN_DIR,"template.html"),os.path.join(MAIN_DIR,"public","index.html"))

if __name__ == "__main__":
    main()
