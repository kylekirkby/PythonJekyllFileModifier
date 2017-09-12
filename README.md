# PythonJekyllFileModifier
A python script to parse a directory/file containing YAML prepended content and create a master editable file. You can then make changes to this file and give it back to the script to make changes.

# Usage 
To use this script simply supply a directory containing jekyll content files using the following:

```bash
python3 jekyll-file-modifier.py _product/
```

The script will then recursively go through the folders within this directory looking for valid jekyll files
and will add the contents of these files to a "master" by default named after the directory you provided.
The master file also gets the original path of the directory added to the front of the master file.
This file can then be modified by anyone and then supplied back to the script as:

```bash
python3 jekyll-file-modifier.py _product.txt
```

After running the above, all changes to the front matter / content of any of the files will be 
changed in the original path.