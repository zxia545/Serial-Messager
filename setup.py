
from setuptools import setup, find_packages
with open('README.md') as f:
    long_description = f.read()

setup(
    name='commsHandler',
    version='0.1.3',
    packages=find_packages(),
    install_requires=['pyserial'],
    author='Tony Xiao',
    author_email='tony.xiao@fisherpaykel.com',
    description='A project for handling serial messaging services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zxia545/Serial-Messager',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)