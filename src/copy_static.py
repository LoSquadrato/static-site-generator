import os
import shutil

from pathlib import Path
from blocks_markdown import *


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    try:
        with open(from_path) as f:
            source = f.read()
    except Exception as e:
        print(f"Cannot read {from_path}:{e}")
    html_string = markdown_to_html_node(source).to_html()
    title_page = extract_title(source)
    try:
        with open(template_path) as t:
            template = t.read()
    except Exception as e:
        print(f"Cannot read {template_path}:{e}")   
    template = template.replace("{{ Title }}", title_page, 1)
    template = template.replace("{{ Content }}", html_string, 1)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    print(f"Successfully update {template_path}")
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        try:            
            os.makedirs(dest_dir)
        except Exception as e:
            print(f"Cannot create directory for {dest_path}: {e}")
    try:        
        with open(dest_path, "w") as d:
            d.write(template)
    except Exception as e:
        print(f"Cannot write {dest_path}: {e}")
    return f"Successfully generate {dest_path}"
    
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    print(f"Generate .html in {dest_dir_path} from .md in {dir_path_content} using {template_path}")
    file_list = os.listdir(dir_path_content)
    for file in file_list:
        file_path_content = os.path.join(dir_path_content, file)
        if os.path.isfile(file_path_content) and ".md" in file:
            dest_file_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
            generate_page(file_path_content, template_path, dest_file_path, basepath)
        elif os.path.isdir(file_path_content):
            try:
                dest_file_path = os.path.join(dest_dir_path, file)
                os.mkdir(dest_file_path)
            except Exception as e:
                print(f"Cannot create {dest_file_path}: {e}")
            generate_pages_recursive(file_path_content, template_path, dest_file_path, basepath)#verifico ricorsività simile a copy static
    return f"All file .html in {dest_dir_path} successfully created"

def copy_static(public_path, static_path):
    print(f"Start copying dir from {public_path} to {static_path}")
    if os.path.exists(public_path) is True:
        try:
            shutil.rmtree(public_path)
            print(f"remove old public dir!")
        except PermissionError:
            print("Permission denied.")
        except Exception as e:
            print(f"Error occurred: {e}")
        
    try:
        os.mkdir(public_path)
        print(f"create new public dir!")
    except PermissionError:
        print("Permission denied.")
    except Exception as e:
        print(f"Error occurred: {e}") 

    print("Before copying file:")
    copy_file = copy_file_list(public_path, static_path)
    return copy_file

def copy_file_list(destination, source):
    file_list = os.listdir(source)    
    for file in file_list:
        source_path = os.path.join(source, file)
        destination_path = os.path.join(destination, file)
        if os.path.isfile(source_path):
            try:
                shutil.copy(source_path, destination_path)
                print(f"File {file} copied successfully to {destination_path}.")
            except shutil.SameFileError:
                print("Source and destination represents the same file.")
            except PermissionError:
                print("Permission denied.")
            except Exception as e:
                print(f"Error copying file {file}: {e}")
        elif os.path.isdir(source_path):
            try:
                if not os.path.exists(destination_path):
                    try:
                        os.makedirs(destination_path)
                        print(f"Directory {file} created successfully.")
                    except PermissionError:
                        print("Permission denied.")
                    except Exception as e:
                        print(f"Error copying file {file}: {e}")
                copy_file_list(destination_path, source_path)
            except PermissionError:
                    print("Permission denied.")
            except Exception as e:
                print(f"Error copying file {file}: {e}")

    return f"All files and directories copied to {destination}."


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            title = block.replace("# ","", 1)
    return title

