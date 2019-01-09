'''
This is a script that update i18n recursively in current folder.

@date 2015-05-26
@author Hong-She Liang <starofrainnight@gmail.com>
'''

import os.path
import glob
import fnmatch
import sys
import io
from rabird.qt.utils import getToolPath


def unix_normpath(path):
    return os.path.normpath(path).replace("\\", "/")


def i18n_update():
    project_file_name = "__i18n_update_project.pro"

    # Get all ui files
    all_py_files = []
    all_ui_files = []
    all_ts_files = []

    default_ts_content = r"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="1.1">
</TS>
"""

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
            elif fnmatch.fnmatch(afile, "*.ts"):
                if os.path.exists(afile_path):
                    statinfo = os.stat(afile_path)
                    if statinfo.st_size <= 0:
                        with io.open(afile_path, "wb") as afile:
                            afile.write(default_ts_content.encode("utf-8"))

                all_ts_files.append(unix_normpath(afile_path))

    # Generate project file
    with io.open(project_file_name, "wb") as project_file:

        content = "SOURCES = \\\n"
        for py_file in all_py_files:
            content += "\t%s \\\n" % py_file
        content += "\n"

        content += "TRANSLATIONS = \\\n"
        for ts_file in all_ts_files:
            content += "\t%s \\\n" % ts_file
        content += "\n"

        content += "FORMS    = \\\n"
        for ui_file in all_ui_files:
            content += "\t%s \\\n" % ui_file
        content += "\n"
        project_file.write(content.encode('utf-8'))
        project_file.close()

        # Really update i18n
        lupdate_path = getToolPath("lupdate")

        i18n_update_command = "\"%s\" -verbose %s" % (
            lupdate_path, project_file_name)
        print(i18n_update_command)
        os.system(i18n_update_command)

    # After all we clear the temporary project file
    os.remove(project_file_name)
