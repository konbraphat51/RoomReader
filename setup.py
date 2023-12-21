from setuptools import find_packages, setup


def requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()


setup(
    name="RoomReader",
    version="0.0.1",
    description="project_description",
    url="https://github.com/author_name/project_urlname/",
    long_description="a",
    long_description_content_type="text/markdown",
    author="author_name",
    requires=requirements(),
    packages=find_packages(),
    install_requires=[],
    entry_points={
        #        "console_scripts": ["project_name = project_name.__main__:main"]
    },
)
