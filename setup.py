import os
import codecs
import logging
import sys
from shutil import rmtree
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))


with open("README.md", "r") as fh:
    long_description = fh.read()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(name)s %(message)s', level='DEBUG')

        # import here, cause outside the eggs aren't loaded
        import pytest
        import six

        args = [self.pytest_args] if isinstance(
            self.pytest_args, six.string_types) else list(self.pytest_args)
        # args.extend(['--cov', 'arctic',
        #              '--cov-report', 'xml',
        #              '--cov-report', 'html',
        #              '--junitxml', 'junit.xml',
        #              ])
        errno = pytest.main(args)
        sys.exit(errno)


class UploadCommand(Command):
    """Support setup.py publish."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds...")
            rmtree(os.path.join(here, "dist"))
        except FileNotFoundError:
            pass
        self.status("Building Source distribution...")
        os.system("{0} setup.py sdist bdist_wheel".format(sys.executable))
        self.status("Uploading the package to PyPi via Twine...")
        os.system("sudo twine upload dist/*")
        sys.exit()



setup(
    name="funguauniverse",
    version="0.1.8",
    author="Kevin Hill",
    author_email="kah.kevin.hill@gmail.com",
    description="A set of class tools to run the Funguana Pipeline. Many irrelelavent parts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["funguauniverse"],
    install_requires=['pytest', 'scipy', 'numpy', 'pandas', 'dask[complete]',
                      'ta-lib', 'loguru', 'spaceman', 'prometheus-client'],
    packages=find_packages(exclude=['scripts']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={"upload": UploadCommand, "test": PyTest},
)
