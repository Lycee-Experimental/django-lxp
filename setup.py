import subprocess
import sys
from setuptools import setup
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
setup(
    name="django-lxp",
    version="1.0",
)