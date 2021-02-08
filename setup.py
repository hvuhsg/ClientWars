from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
setup(
    name="ClientWars",
    packages=["client_wars"],
    include_package_data=True,
    version="v1.1",
    license="MIT",
    description="War game, but for programmers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="yoyo",
    author_email="serverwars00@gmail.com",
    url="https://github.com/hvuhsg/ClientWars",
    download_url="",
    keywords=[
        "game",
        "war",
        "programming",
        "win"
    ],  # Keywords that define your package best
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    
)