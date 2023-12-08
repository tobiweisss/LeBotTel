import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="LeBotTel",                        # This is the name of the package
    version="0.2.0",                        # The initial release version
    author="Antonio Vidos, Tobias Lettner, Tobias Weiß, Uwe Kölbel",
    author_email="",                        # TODO: Add the email address here
    description="A simple Telegram Bot",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.9',                # Minimum version requirement of the package
    py_modules=["LeBotTel"],                # Name of the python package
    package_dir={'':'LeBotTel'},            # Directory of the source code of the package
    install_requires=required               # Install other dependencies if any
)