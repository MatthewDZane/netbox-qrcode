import codecs
import os.path

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='netbox-qrcode',
    version=get_version('netbox_qrcode/version.py'),
    description='QR Code generation for netbox objects',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/k01ek/netbox-qrcode',
    author='Nikolay Yuzefovich',
    author_email='mgk.kolek@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.ttf'],
        '': ['*.html'],
    },
    install_requires=[
        'qrcode',
        'Pillow'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ]
)
