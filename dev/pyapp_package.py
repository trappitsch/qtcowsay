# Creates a package using PyApp

import importlib.metadata
import os
from pathlib import Path, PurePath
import shutil
import subprocess
import tarfile
from urllib.request import urlretrieve

PYAPP_SOURCE = "https://github.com/ofek/pyapp/releases/latest/download/source.tar.gz"


def package(module_name: str, build_manager: str = "rye"):
    """Creates the package with PyApp.

    :param module_name: The module to package.
    :param build_manager: The build manager to use. Defaults to rye.
        Currently, only "rye" is supported.

    """
    _check_requirements()
    dist_path = _build(build_manager)
    pyapp_path = _get_pyapp()
    _set_up_env(module_name, dist_path, pyapp_path)
    _package_app(pyapp_path, module_name)


def _build(build_manager: str) -> Path:
    """Build the package with PyApp and set the package path.

    :param build_manager: The build manager to use. Defaults to rye.

    :return: The path to the packaged module.
    """

    if build_manager != "rye":
        print(f"Error: {build_manager} is not supported. Please use rye.")
        raise SystemExit(1)

    print(f"Building package with {build_manager}...")
    # build the package
    try:
        subprocess.run(
            [build_manager, "build"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print(
            f"Error: {build_manager} not found. Please install {build_manager} and try again."
        )
        raise SystemExit(1)

    # return the package path - fixme: this is a hack and rye only
    return Path(PurePath(__file__).parents[1]).joinpath("dist")


def _check_requirements():
    """Check if all requirements are installed."""
    # check for cargo
    try:
        subprocess.run(
            ["cargo", "--version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("Error: cargo not found. Please install cargo and try again.")
        raise SystemExit(1)


def _get_module_version(module_name: str) -> str:
    """Get the version of the module.

    :param module_name: The name of the module to get the version of.

    :return: The version of the module.
    """
    return importlib.metadata.version(module_name)


def _get_pyapp() -> Path:
    """Get the latest version of PyApp and extract it.

    :return: The path to the extracted PyApp source.
    """
    # remove old versions of pyapp folders
    for file in Path(".").iterdir():
        if file.is_dir() and file.name.startswith("pyapp-"):
            shutil.rmtree(file)

    # download the latest version of pyapp as pyapp-source.tar.gz
    urlretrieve(PYAPP_SOURCE, "pyapp-source.tar.gz")

    # extract the source with tarfile package as pyapp-latest
    with tarfile.open("pyapp-source.tar.gz", "r:gz") as tar:
        tar.extractall()

    # find the name of the pyapp folder and return it
    for file in Path(".").iterdir():
        if file.is_dir() and file.name.startswith("pyapp-"):
            return file


def _package_app(pyapp_path: Path, module_name: str):
    """Package the app and move it to the dev folder."""

    print("Packaging app with cargo...")
    # run cargo build --release with subprocess in the pyapp folder
    subprocess.run(
        ["cargo", "build", "--release"],
        cwd=pyapp_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # move package to dev folder and rename it to module_name
    shutil.move(
        pyapp_path.joinpath("target/release/pyapp"),
        Path(__file__).parent.joinpath(module_name),
    )


def _set_up_env(module_name: str, dist_path: Path, pyapp_path: Path):
    """Set up the environment for packaging the module.

    :param module_name: The name of the module to package.
    :param dist_path: The path to the packaged module.
    :param pyapp_path: The path to the extracted PyApp source.
    """
    # remove all environment variables that start with PYAPP
    for key in list(os.environ):
        if key.startswith("PYAPP"):
            del os.environ[key]

    mod_version = _get_module_version(module_name)
    module_whl = dist_path.joinpath(f"{module_name}-{mod_version}-py3-none-any.whl")

    # copy the wheel to the pyapp folder
    shutil.copy(module_whl, pyapp_path)

    # setup environment
    os.environ["PYAPP_PROJECT_NAME"] = module_name
    os.environ["PYAPP_PROJECT_VERSION"] = mod_version
    os.environ["PYAPP_PROJECT_PATH"] = module_whl.name
    os.environ["PYAPP_EXEC_SPEC"] = f"{module_name}:run"


if __name__ == "__main__":
    package("qtcowsay")
