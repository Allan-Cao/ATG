from setuptools import setup, find_packages

setup(
    name="ATG",
    version="0.1.0.1",
    packages=find_packages(include=["ATG", "ATG.*"]),
    install_requires=[
        "SQLAlchemy",
        "tqdm",
        "backoff",
        "psycopg2-binary",
        "ratelimit",
        "requests",
    ],
    python_requires=">=3.10",  # Union typing is extensively used.
)
