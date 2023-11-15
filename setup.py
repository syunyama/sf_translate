from setuptools import setup, find_packages

with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="sf_translate",
    version="0.0.1",
    author='syunyama',
    author_email='sample@example.com',
    url='https://github.com/syunyama/sf_translate',
    packages=find_packages(),
    install_requires=install_requirements,
    entry_points={"console_scripts": ["sf_translate = command:main"]},
)
