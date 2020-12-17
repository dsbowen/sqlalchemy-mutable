import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-mutable",
    version="0.0.11",
    author="Dillon Bowen",
    author_email="dsbowen@wharton.upenn.edu",
    description="A powerful and flexible SQLAlchemy database type for nested mutation tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dsbowen.github.io/sqlalchemy-mutable/",
    packages=setuptools.find_packages(),
    install_requires=[
        'sqlalchemy>=1.3.12',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)