from setuptools import setup, find_packages

setup(
    name="gdapi",
    version="1.0.0",
    description="An asynchronous wrapper for Geometry Dash.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="notanerd",
    url="https://github.com/notanerd/geometrydash",
    packages=find_packages(),
    install_requires=["httpx"],
    license="MIT License",
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)