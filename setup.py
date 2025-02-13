from setuptools import setup, find_packages

setup(
    name="ATG",
    version="1.0.2.0",
    packages=find_packages(include=["ATG", "ATG.*"]),
    install_requires=[
        "SQLAlchemy",
        "tqdm",
        "backoff",
        "psycopg2",
        "ratelimit",
        "requests",
    ],
    python_requires=">=3.10",  # Union typing is extensively used.
)
