from setuptools import find_packages, setup

setup(
    name="rc4me",
    author="Michael Stefferson/Jeffrey Moore",
    author_email="na@gmail.com",
    description="Description",
    url="",
    version="0.0.0",
    packages=find_packages(),
    install_requires=["click>=7.1.2"],
    python_requires=">=3.8",
    license="MIT License",
    entry_points="""
        [console_scripts]
        rc4me=rc4me.run:cli
    """,
)
