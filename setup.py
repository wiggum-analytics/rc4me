from setuptools import find_packages, setup

setup(
    name="rc4me",
    author="Michael Stefferson/Jeffrey Moore",
    author_email="mstefferson@gmail.com",
    description="Description",
    packages=find_packages(),
    install_requires=["click>=7.1.2", "pick>=1.0.0", "gitpython>=3.1.11"],
    python_requires=">=3.8",
    license="MIT License",
    entry_points="""
        [console_scripts]
        rc4me=rc4me.cli:cli
    """,
)
