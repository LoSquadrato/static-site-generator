import sys


from copy_static import copy_static, generate_pages_recursive

static_path = "./static"
public_path = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    copy_static_result = copy_static(public_path, static_path)
    generate_page_result = generate_pages_recursive(dir_path_content, template_path, public_path, basepath)
    print(generate_page_result)


main()
