import os.path
import importlib
import inspect
import glob
import tempfile
import xml.etree.ElementTree as etree
from rabird.qt.utils import getToolPath


def auto_compile_uis(ui_dir):
    '''
    Compile all UI's in specific directory if they are not compiled or
    changed.
    '''
    ui_paths = glob.glob(os.path.join(ui_dir, "*.ui"))
    for ui_path in ui_paths:
        xml_tree = etree.ElementTree()
        xml_tree.parse(ui_path)

        class_name = xml_tree.find("class").text
        ui_name = os.path.splitext(os.path.basename(ui_path))[0]

        # Fix name for ui_name
        xml_tree.find("class").text = ui_name
        xml_tree.find("widget").attrib["name"] = ui_name

        temp_ui_file_path = ui_path
        if ui_name != class_name:
            temp_ui_file = tempfile.NamedTemporaryFile(delete=False)
            temp_ui_file_path = temp_ui_file.name
            temp_ui_file.write(etree.tostring(
                xml_tree.getroot(), encoding="utf-8"))
            temp_ui_file.close()

        compiled_ui_path = os.path.join(ui_dir, "Ui_%s.py" % ui_name)
        uic_path = getToolPath("uic")
        compie_command = "%s %s -o %s" % (
            uic_path, temp_ui_file_path, compiled_ui_path)

        # Only compile newer files
        if ((compiled_ui_path is not None) and
                os.path.exists(compiled_ui_path)):

            compiled_ui_stat = os.stat(compiled_ui_path)
            ui_stat = os.stat(ui_path)

            # If compiled ui file different from ui file, we should
            # recompile it.
            if ((compiled_ui_stat.st_mtime < ui_stat.st_mtime) or
                    (compiled_ui_stat.st_size != ui_stat.st_size)):
                os.system(compie_command)
        else:
            os.system(compie_command)


def import_uis():
    '''
    Import all UIs in directory where invoker's module stay.

    Normally, this function will invoke in the module's __init__.py, for
    ex:

    __init__.py:

    @code
    import rabird.qt

    # This method will import all UI's located in this module's directory.
    rabird.qt.import_uis()
    @endcode
    '''
    suffixs = ["pyo", "pyc", "py"]

    # Get outter frame
    outer_frame = inspect.stack()[1]
    outer_module = inspect.getmodule(outer_frame[0])

    outer_module_dir = os.path.dirname(os.path.abspath(outer_module.__file__))

    auto_compile_uis(outer_module_dir)

    compiled_ui_paths = []
    for suffix in suffixs:
        compiled_ui_paths += glob.glob(os.path.join(
            outer_module_dir, "Ui_*.%s" % suffix))

    for compiled_ui_path in compiled_ui_paths:
        module_name = os.path.splitext(
            os.path.basename(compiled_ui_path))[0][3:]
        if module_name in outer_module.__dict__:
            continue

        module_full_name = "%s.%s" % (outer_module.__name__, module_name)

        # Import the module
        if module_name not in importlib.import_module(module_full_name).__dict__:
            raise AttributeError("There do not have class '%s' in module '%s',"
                                 " Please check the class name !"
                                 % (module_name, module_full_name))

        outer_module.__dict__[module_name] = importlib.import_module(
            module_full_name).__dict__[module_name]
