import frontmatter
import sys
import os
import shutil
from io import BytesIO
import glob


def write_seo_data_to_csv(my_directory):
    md_files = directory_frontmatter(my_directory, output=False)

def parse_new_changes(my_file):
    """
    Takes a .txt file as input and reads new changes
    """
    with open(my_file) as change_file:

        string_data = change_file.read()

        separator = "\n" + ("=" * 40) + "\n"
        
        data = string_data.split(separator)
        
        original_path = data[0]
        
        md_files = directory_frontmatter(original_path, output=False)
        
        for each in md_files:
            frontmatter_check = frontmatter.loads(open(each,"r").read())
            if "permalink" in frontmatter_check.keys():
                for changes in data[1:]:
                    fm = frontmatter.loads(changes)
                    if "permalink" in fm.keys():
                        if frontmatter_check["permalink"] == fm["permalink"]:
                            # Compare files and change if necessary
                            changed = False
                            change_list = []
                            # print("Checking for changes to {0} front matter".format(frontmatter_check["permalink"]))
                            for key in frontmatter_check.keys():
                                if frontmatter_check[key] != fm[key]:
                                    frontmatter_check[key] = fm[key]
                                    changed = True
                                    change_list.append(key)
                            # print("Checking for changes to {0} content".format(frontmatter_check["permalink"]))
                            if frontmatter_check.content != fm.content:
                                frontmatter_check.content = fm.content
                                changed = True
                                change_list.append("Content")
                            if changed:
                                with open(each,"w") as new_file:
                                    new_file.writelines(frontmatter.dumps(frontmatter_check))
                                    # frontmatter.dump(frontmatter_check, new_file)
                                    print("{0} changed for {1}".format(str(change_list), frontmatter_check["permalink"]))
    
    print("Parsing complete.")

    
        
def file_frontmatter(my_file):
    """
    Takes a filename as input and writes front matter to csv named after file
    """
    
    split_filename = my_file.split(".")
    
    name_without_ext = split_filename[0]
    
    csv_file = name_without_ext + ".csv"
    csv_file_path = csv_file.split("/")
    csv_file_new_name = csv_file_path[-1]
    
    csv_new_path = os.getcwd() + "/" + csv_file_new_name
    
    print(csv_new_path)
        
    # Load the front matter file
    markdown_file = frontmatter.load(my_file)
    
    fm = frontmatter.dumps(markdown_file)
    
    print("Writing to {0}...".format(csv_file))
    
    with open(csv_new_path, "w") as new_csv_file:
        new_csv_file.writelines(fm)
        
    print("Done!")
    
def directory_frontmatter(my_directory, output=True):
    """
    Takes a directory as input and loops through folder looking for front matter 
    and appends each to csv named after containing directory
    """
    types = [".md",".markdown",".mdown"]
    
    if my_directory.endswith("/"):
        directory_name = my_directory.split("/")[-2]
    else:
        directory_name = my_directory.split("/")[-1]
    
    directory_output_file = os.getcwd() +  "/" + directory_name + ".txt"
        
    # Loop through all find all markdown files
    markdown_files = []
    for t in types:
        for markdown_file in glob.iglob('{0}/**/*{1}'.format(my_directory,t), recursive=True):
            markdown_files.append(markdown_file)
    
    if output == True:
        with open(directory_output_file, "w") as output_file:
            output_file.write(my_directory)
            for each in markdown_files:
                contents = frontmatter.load(each)
                fm = frontmatter.dumps(contents)
                separator = "\n" + ("=" * 40) + "\n"
                output_file.write(separator)
                output_file.writelines(fm)
        print("Done!")
    else:
        return markdown_files
    
def main():
    
    # Get the last argument from the sys arguments.
    input_file = sys.argv[-1]
    
    # Check if input is a file or directory
    is_file = os.path.isfile(input_file)
    if input_file != "frontmatter-collector.py":
        if is_file:
            # Check to see if the input file is a .txt file
            if input_file.endswith(".txt"):
                parse_new_changes(input_file)
            else:
                file_frontmatter(input_file)    
        else:
            directory_frontmatter(input_file)
    else:
        print("Please supply a path to file or directory to collect contents.")
        
        
if __name__ == "__main__":
    main()