import setuptools


setuptools.setup(
    name="musiclang",
    version="0.0.1",
    author="Florian GARDIN",
    author_email="fgardin.pro@gmail.com",
    description=("A python package for music notation and generation"
                ),
    long_description="A python package for music notation and generation",
    long_description_content_type="text/markdown",
    url="",
    project_urls={
        "Bug Tracker": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"

                      ],
    packages=setuptools.find_packages(include='*'),
    package_data={'datadoc': ['templates/*.txt']},
    include_package_data=True,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "datadoc = datadoc.cli:main",
        ]
    }
)