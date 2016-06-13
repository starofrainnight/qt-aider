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

    for ts_file in glob.glob("./i18n/*.ts"):
        all_ts_files.append(unix_normpath(ts_file))

    # Get all translation files
    all_ui_files = []

    for root, dirs, files in os.walk(os.curdir):
        for afile in files:
            if not fnmatch.fnmatch(afile, "*.py"):
                continue

            # Skip generated Ui_*.py
            if fnmatch.fnmatch(afile, "Ui_*.py"):
                continue

            afile = unix_normpath(os.path.join(root, afile))
            all_py_files.append(afile)

    # Generate project file
    project_file = open(project_file_name, "wb")

    project_file.write("SOURCES = \\\n")
    for py_file in all_py_files:
        project_file.write("\t%s \\\n" % py_file)
    project_file.write("\n")

    project_file.write("TRANSLATIONS = \\\n")
    for ts_file in all_ts_files:
        project_file.write("\t%s \\\n" % ts_file)
    project_file.write("\n")

    project_file.write("FORMS    = \\\n")
    for ui_file in all_ui_files:
        project_file.write("\t%s \\\n" % ui_file)
    project_file.write("\n")

    project_file.close()

    # Really update i18n
    pyside_dir = os.path.dirname(PySide.__file__)
    if sys.platform == "win32":
        pyside_lupdate_path = os.path.join(pyside_dir, "pyside-lupdate.exe")
    else:
        pyside_lupdate_path = os.path.join(pyside_dir, "pyside-lupdate")

    i18n_update_command = "\"%s\" %s" % (
        pyside_lupdate_path, project_file_name)
    print(i18n_update_command)
    os.system(i18n_update_command)
