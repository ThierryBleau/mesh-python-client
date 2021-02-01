import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mesh-python",
    version="0.1",
    author="Thierry Bleau",
    author_email="thierry@protean.so",
    description="Python client to query the mesh engine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'pandas'
    ],
    keywords='crypto ethereum python client uniswap graph'
)