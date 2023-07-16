from os import path
from setuptools import setup

from linxdot_exporter.version import __version__

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), "r", encoding = "utf-8") as f:
    long_description = f.read()

setup(
    name="linxdot_exporter",
    version=__version__,
    author="Gustavo Oliveira",
    author_email="cetres@gmail.com",
    description="Prometheus exporter for Linxdot Helium miner",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache Software License 2.0",
    keywords="prometheus monitoring exporter",
    url="https://github.com/cetres/linxdot_exporter",
    packages=[
        'linxdot_exporter',
    ],
    install_requires=[         
        'prometheus_client',
        'requests'
    ],
    extras_require={
        'twisted': ['twisted'],
    },
    test_suite="tests",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: Apache Software License",
    ],
)