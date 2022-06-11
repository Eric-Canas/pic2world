from setuptools import setup, find_packages

setup(
    name='pic2world',
    version='0.1',
    packages=find_packages('modules'),
    url='https://github.com/Eric-Canas/pic2world',
    license='MIT',
    package_dir={'': 'modules'},
    author='Eric Canas',
    author_email='eric@ericcanas.com',
    description='P2W is a toolbox that implements several utilities for getting real-world information from pictures.',
    install_requires=[
        'numpy',
    ],
)
