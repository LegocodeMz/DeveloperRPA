from setuptools import setup, find_packages

setup(
    name="challenge_rpa_dev",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
