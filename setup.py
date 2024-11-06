from setuptools import setup, find_packages

setup(
    name="SQDBI",
    version="0.0.4.1",
    packages=find_packages(include=["SQDBI", "SQDBI.*"]),
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
