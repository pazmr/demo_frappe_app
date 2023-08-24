from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in erpnext_mastery/__init__.py
from erpnext_mastery import __version__ as version

setup(
	name="erpnext_mastery",
	version=version,
	description="ERPNEXT API Series",
	author="Max Paz",
	author_email="maxpaz2004@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
