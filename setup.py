from setuptools import setup

__version__ = "1.0.7"

setup(
    name="pyfujitsugeneral",
    py_modules=["pyfujitsugeneral"],
    version=__version__,
    description="Python Library for interacting with Fujitsu General split air conditioners API",
    long_description="Python Library for interacting with Fujitsu General split air conditioners API",
    author="Fabio Mauro, Mehdi Modarressi",
    author_email="bigmoby.pymeianlike@gmail.com",
    url="https://github.com/bigmoby/pyfujitsugeneral",
    download_url="https://github.com/bigmoby/pyfujitsugeneral",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["Fujitsu General air conditioners"],
    packages=["pyfujitsugeneral"],
    include_package_data=True,
    install_requires=["requests", "certifi", "chardet", "idna", "urllib3"],
)
