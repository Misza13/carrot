from setuptools import setup

setup(
    name='carrot',
    version='0.1',
    description='Command-line Minecraft mod manager',
    author='Misza',
    author_email='misza@misza.net',
    license='MIT',
    packages=['carrot'],
    entry_points={
        'console_scripts': [
            'carrot = carrot.cli:main'
        ]
    }
)