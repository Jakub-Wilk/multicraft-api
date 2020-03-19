import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multicraft-api", # Replace with your own username
    version="1.3.1",
    author="Jakub Wilk",
    author_email="wilkjakub64@gmail.com",
    description="A Python port of the Multicraft API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jakub-Wilk/MulticraftAPI.py",
    packages=[
        'multicraftapi'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)