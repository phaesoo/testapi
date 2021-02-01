from setuptools import setup


setup(
    name='testapi',
    version='1.0.0',
    author='phaesoo',
    packages=['app'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
