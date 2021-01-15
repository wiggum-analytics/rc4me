from setuptools import find_packages, setup

setup(
    name="rc4me",
    author="Michael Stefferson/Jeffrey Moore",
    author_email="na@gmail.com",
    description="Description",
    url="",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["Click"],
    license="MIT License",
    entry_points="""
        [console_scripts]
        rc4mw=rc4me.run:cli
    """
)
