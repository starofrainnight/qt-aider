'''
This is a script that update i18n recursively in current folder.

@date 2015-05-26
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os.path
import glob
import fnmatch
import PySide
import sys
import io

def unix_normpath(path):
    return os.path.normpath(path).replace("\\", "/")


def i18n_update():
    project_file_name = "__i18n_update_project.pro"

    # Get all ui files
    all_py_files = []
    all_ui_files = []

    for root, dirs, files in os.walk(os.curdir):
        for afile in files:
            afile_path = unix_normpath(os.path.join(root, afile))
            if fnmatch.fnmatch(afile, "*.py"):
                # Skip generated Ui_*.py
                if fnmatch.fnmatch(afile, "Ui_*.py"):
                    continue

                all_py_files.append(afile_path)
            elif fnmatch.fnmatch(afile, "*.ui"):
                all_ui_files.append(afile_path)

    # Get all translation files
    all_ts_files = []

    default_ts_content = r"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="1.1">
</TS>
"""
    for ts_file in glob.glob("./i18n/*.ts"):
        if os.path.exists(ts_file):
            statinfo = os.stat(ts_file)
            if statinfo.st_size <= 0:
                with io.open(ts_file, "wb") as afile:
                    afile.write(default_ts_content.encode("utf-8"))

        all_ts_files.append(unix_normpath(ts_file))

    # Generate project file
    project_file = io.open(project_file_name, "wb")

    content = "SOURCES = \\\n"
    for py_file in all_py_files:
        content += "\t%s \\\n" % py_file
    content += "\n"

    content += "TRANSLATIONS = \\\n";
    for ts_file in all_ts_files:
        content += "\t%s \\\n" % ts_file;
    content += "\n"

    content += "FORMS    = \\\n"
    for ui_file in all_ui_files:
        content += "\t%s \\\n" % ui_file
    content += "\n"
    project_file.write(content.encode('utf-8'))
    project_file.close()

    # Really update i18n
    pyside_dir = os.path.dirname(PySide.__file__)
    if sys.platform == "win32":
        pyside_lupdate_path = os.path.join(pyside_dir, "pyside-lupdate.exe")
    else:
        pyside_lupdate_path = os.path.join(pyside_dir, "pyside-lupdate")
    if not os.path.exists(pyside_lupdate_path):
        pyside_lupdate_path = "pyside-lupdate"

    i18n_update_command = "\"%s\" %s" % (
        pyside_lupdate_path, project_file_name)
    print(i18n_update_command)
    os.system(i18n_update_command)
