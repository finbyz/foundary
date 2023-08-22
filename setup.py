from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in foundary/__init__.py
from foundary import __version__ as version

setup(
	name="foundary",
	version=version,
	description="foundary app",
	author="Finbyz Tech PVT LTD",
	author_email="info@finbyz.tech",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
