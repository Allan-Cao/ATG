from setuptools import setup, find_packages

setup(
    name="ATG",
    version="1.2.1.1",
    packages=find_packages(include=["ATG", "ATG.*"]),
    install_requires=[
        "SQLAlchemy",
        "tqdm",
        "psycopg[binary]",
        "requests",
    ],
    python_requires=">=3.10",  # Union typing is extensively used.
)
