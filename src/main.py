import os, shutil, sys
from pathlib import Path

from textnode import TextNode, TextType
from block_markdown import markdown_to_html_node, extract_title

def main():
    build_basepath = Path(__file__).resolve().parent.parent
    print(build_basepath)
    dest_basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    content_dir = Path(os.path.join(build_basepath, "content"))
    static_dir = Path(os.path.join(build_basepath, "static"))
    template_dir = Path(os.path.join(build_basepath, "template.html"))
    doc_dir = Path(os.path.join(build_basepath, "docs"))
    doc_dest_dir = Path(os.path.join(dest_basepath, "docs"))


    clear_directory(doc_dir)
    copy_directory(static_dir, doc_dir)
    generate_all_pages(content_dir, template_dir, doc_dir, doc_dest_dir)

def clear_directory(path):
    if os.path.exists(path):
        for child in Path(path).iterdir():
            if Path.is_dir(child):
                clear_directory(child)
                shutil.rmtree(child)
            else:
                os.unlink(child)


def copy_directory(source, target):
    if not os.path.exists(source):
        os.makedirs(source, exist_ok=True)
        return
    
    if not os.path.exists(target):
        os.makedirs(target, exist_ok=True)
    
    for child in os.listdir(source):
        source_loc = Path(os.path.join(source, child))
        target_loc = Path(os.path.join(target, child))
        print(f"Copying: {source_loc} to {target_loc}")
        if Path.is_dir(source_loc):
            if not os.path.exists(target_loc):
                os.makedirs(target_loc, exist_ok=True)
            copy_directory(source_loc, target_loc)
        else:
           shutil.copy(source_loc, target_loc)

           
def generate_all_pages(dir_path_content, template_path, dest_dir_path, base_path):
    source_dir = Path(dir_path_content)
    template_dir = Path(template_path)
    dest_dir = Path(dest_dir_path)

    for md_path in source_dir.rglob("*.md"):
        rel_path = md_path.relative_to(source_dir).parent
        page_dest_path = dest_dir / rel_path
        generate_page(md_path, template_dir, page_dest_path, base_path)



def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    if not os.path.exists(from_path):
        raise ValueError(f"no file exists at {from_path}")

    if not os.path.exists(dest_path):
        os.makedirs(dest_path,exist_ok=True)
    with open(from_path, "r+") as source_content_stream:
        source_content = source_content_stream.read()
        source_title = extract_title(source_content)
        source_html = markdown_to_html_node(source_content).to_html()

    with open(template_path) as template_content_stream:
        page_html = template_content_stream.read()
        page_html = page_html.replace("{{ Title }}", source_title, 1)
        page_html = page_html.replace("{{ Content }}", source_html, 1)
        page_html = page_html.replace('href="/', f'href="{base_path}')
        page_html = page_html.replace('src="/', f'src="{base_path}')

    with open(os.path.join(dest_path, "index.html"), "w") as page_content_stream:
        page_content_stream.write(page_html)


    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)


main()