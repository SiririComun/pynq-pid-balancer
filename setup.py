import os
import shutil
from setuptools import setup, find_packages
from pynq.utils import build_py

module_name = "balancin"

# 1. Automatically copy the user notebooks into the package for distribution
if os.path.exists("notebooks"):
    dest_dir = os.path.join(module_name, "notebooks")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree("notebooks", dest_dir)

# 2. Helper function to find all non-Python assets (bitstreams, hwh, notebooks)
data_files = []
def extend_package(path):
    if os.path.isdir(path):
        data_files.extend(
            [os.path.join("..", root, f) for root, _, files in os.walk(path) for f in files]
        )

# Map the bitstreams and notebooks for setuptools packaging
extend_package(os.path.join(module_name, "bitstreams"))
extend_package(os.path.join(module_name, "notebooks"))

# 3. Standard Setup configuration
setup(
    name=module_name,
    version="1.0.0",
    description="Real-time PID Balancer Overlay and Interactive Dashboard",
    author="Pablo Sanchez & Software Team",
    packages=find_packages(),
    package_data={
        "": data_files,
    },
    install_requires=[
        "pynq>=2.7.0"
    ],
    entry_points={
        "pynq.notebooks": [
            "balancin = balancin.notebooks"
        ]
    },
    cmdclass={"build_py": build_py}
)