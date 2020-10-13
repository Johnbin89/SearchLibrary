import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="search-jbin", # Replace with your own username
    version="0.0.1",
    author="jbin",
    author_email="john_biniaris@hotmail.com",
    description="A library of searh algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['search'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)