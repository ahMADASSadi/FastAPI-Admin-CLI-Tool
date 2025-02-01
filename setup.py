from setuptools import setup, find_packages

setup(
    name="fact",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "typing",
        "typer",
        "jinja2",
        "sqlmodel",
        "asyncpg",
        "jose",
    ],
    entry_points={
        "console_scripts": [
            "fact=fastapi_admin.main:main",
        ],
    },
    description="A User Friendly CLI tool for FastAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ahMAD ASSadi",
    author_email="madassandd@gmail.com",
    url="ahMADASSadi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
)
