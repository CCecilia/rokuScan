import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rokuScan",
    version="0.0.1",
    py_modules=['rokuScan'],
    install_requires=[
        'Click',
        'urllib3'
    ],
    entry_points='''
        [console_scripts]
        rokuScan=rokuScan:scan
    ''',
    author="Christian Cecilia",
    author_email="christian.cecilia1@gmail.com",
    description="A simple pip package for scanning networks for Roku's.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CCecilia/rokuScan.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)