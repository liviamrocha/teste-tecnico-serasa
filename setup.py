import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="credito",
    version="0.1.0",
    description="Busca por melhores ofertas de empréstimos entre os parceiros do Serasa Crédito",
    url="credito.io",
    python_requires=">=3.8",
    long_description="Busca por melhores ofertas de empréstimos entre os parceiros do Serasa Crédito",
    long_description_content_type="text/markdown",
    author="Lívia Rocha",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["credito = credito.cli:main"]
    }
)