from setuptools import setup, find_packages

setup(
    name="fastapi-admin",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "typing",
        "typing_extensions",
        "typer",
    ],
    entry_points={
        "console_scripts": [
            "fastapi-admin=fastapi_admin.cli:main",
        ],
    },
    description="A User Friendly project manager/creator for FastAPI Project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/fastapi-admin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)