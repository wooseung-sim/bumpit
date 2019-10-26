from setuptools import setup, find_packages

with open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="gobump",
    version="0.0.0",
    description="A CLI tool bumps versions in tracked files.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mobiusbyte/gobump",
    project_urls={
        "Code": "https://github.com/mobiusbyte/gobump",
        "Issue tracker": "https://github.com/mobiusbyte/gobump/issues",
    },
    license="MIT",
    author="Jill San Luis",
    author_email="jill@mobiusbyte.com",
    packages=find_packages(),
    entry_points={"console_scripts": ["gobump=gobump.console.cli:main"]},
    include_package_data=True,
    install_requires=["click"],
    extras_require={"test": ["pytest"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
)