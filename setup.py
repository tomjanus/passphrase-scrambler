""" Runner of the setup method with configuration given in setup.cfg """
import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    """ Function for reading text files """
    with io.open(join(dirname(__file__), *names),
                 encoding=kwargs.get('encoding', 'utf8')) as file_handle:
        return file_handle.read()


if __name__ == '__main__':
    # The use_scm_version option indicates that we want to use the
    # setuptools_scm package to set the version automatically based on git
    # tags, which will produce version strings such as 0.13 for a stable
    # release, or 0.16.0.dev113+g3d1a8747 for a developer version.
    setup(
        name="pass_scrambler",
        version='0.0.0',
        description='Lightweight tool to encode n-word seed passphrases',
        author='Tomasz Janus',
        author_email='tomasz.k.janus@gmail.com',
        url='https://github.com/tomjanus/passphrase_scrambler',
        packages=find_packages('src'),
        package_dir={'': 'src'},
        py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
        include_package_data=True,
        zip_safe=False
    )
