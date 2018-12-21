from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='carrot_mc',
    version='0.3.1',
    description='Command-line Minecraft mod manager',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Misza',
    author_email='misza@misza.net',
    url='https://github.com/Misza13/carrot',
    license='MIT',
    packages=['carrot_mc'],
    entry_points={
        'console_scripts': [
            'carrot = carrot_mc.cli:main'
        ]
    },
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Topic :: Games/Entertainment'
    ]
)