from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
setup(
    name="ClientWars",  # How you named your package folder
    packages=["ClientWars"],  # Chose the same as "name"
    include_package_data=True,
    version="v1.0",  # Start with a small number and increase it with every change you make
    license="MIT",  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="War game, but for programmers.",  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="yoyo",  # Type in your name
    author_email="serverwars00@gmail.com",  # Type in your E-Mail
    url="https://github.com/hvuhsg/ClientWars",  # Provide either the link to your github or to your website
    download_url="",
    keywords=[
        "game",
        "war",
        "programming",
        "win"
    ],  # Keywords that define your package best
    install_requires=requirements,  # I get to this in a second
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    
)