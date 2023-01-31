import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="musiclang",
    version="0.7.1",
    author="Florian GARDIN",
    author_email="fgardin.pro@gmail.com",
    description=("A python package for music notation and generation"
                ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Documentation': 'https://musiclang.readthedocs.io/en/latest/',
        'Source': 'https://github.com/MusicLang/musiclang/',
        'Tracker': 'https://github.com/MusicLang/musiclang/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "lxml==4.9.1",
        "mido==1.2.10",
        "music21==8.1.0",
        "numpy==1.23.4",
        "pandas==1.5.1",
        "scikit-learn==1.1.3",
        "scipy==1.9.3",
        "tensorflow==2.11.0",
        "toml==0.10.2",
        "tomli==2.0.1",
        "xmlschema==2.1.1",
                      ],
    packages=setuptools.find_packages(include='*'),
    package_data={'musiclang': ['augmented_net/*.hdf5']},
    include_package_data=True,
    python_requires=">=3.6",
)