import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-mutable",
    version="0.0.5",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="Generic nested mutable objects and iterables for SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dsbowen/sqlalchemy-mutable",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)