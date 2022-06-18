from amulet_editor.data.packages._manage import enabled_packages, installed_packages
from amulet_editor.models.package import AmuletPackage


def install_package(package: AmuletPackage):
    if not package in installed_packages:
        installed_packages.append(package)


def uninstall_package(package: AmuletPackage):
    if package in installed_packages:
        installed_packages.remove(package)
