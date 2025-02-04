from setuptools import setup, Extension, find_packages
import sys

print(f'Current platform: {sys.platform}')
ext_modules = []
if sys.platform.startswith("linux"):
    ext_modules.append(
        Extension(
            'fastserial',                # The module name (import fastserial)
            sources=['commsHandler/fastserial.c'],  # Adjusted path to the C file
        )
    )

with open('README.md') as f:
    long_description = f.read()

setup(
    name='commsHandler',
    version='0.2.0',
    packages=find_packages(),
    install_requires=['pyserial'],
    ext_modules=ext_modules,
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
