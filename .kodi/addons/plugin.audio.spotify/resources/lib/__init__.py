import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(__file__)))

# IMPORTANT: The 'cherrypy' module cannot be imported as a submodule from 'httpproxy.py'.
#   I.e, 'from deps import cherrypy' will not work. Not sure why. So we do the following
#   path hack to put 'cherrypy' on the module search path:
sys.path.insert(1, os.path.join(os.path.dirname(__file__), "deps"))


# import pkgutil

# def list_submodules(list_name, package_name):
#     for loader, module_name, is_pkg in pkgutil.walk_packages(
#         package_name.__path__, package_name.__name__ + "."
#     ):
#         list_name.append(module_name)
#         print(f"module_name 1 = {module_name}, is_pkg = {is_pkg}.")
#         try:
#             module_name = __import__(module_name, fromlist="dummylist")
#         except Exception as ex:
#             print(ex)
#             module_name = None
#         print(f"module_name 2 = {module_name}.")
#         if is_pkg:
#             list_submodules(list_name, module_name)
#
#
# if len(sys.argv) != 2:
#     print("Usage: {} [PACKAGE-NAME]".format(os.path.basename(__file__)))
#     sys.exit(1)
# else:
#     package_name = sys.argv[1]
#
# print(f"package_name = '{package_name}'.")
# try:
#     package = __import__(package_name)
# except ImportError:
#     print("Package {} not found...".format(package_name))
#     sys.exit(1)
#
# print(f"package.__path__ = '{package.__path__}'.")
# print(f"package.__name__ = '{package.__name__}'.")
#
# all_modules = []
# list_submodules(all_modules, package)
#
# print(f"all_modules = {all_modules}.")
# sys.exit(1)
