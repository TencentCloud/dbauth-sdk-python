from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as f:
    readme = f.read()

VERSION = "v1.0.0"

setup(
    name="tencentcloud-dbauth-sdk-python",
    version=VERSION[1:],
    description="Tencent Cloud DBAuth SDK for Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Tencent Cloud',
    url='https://github.com/TencentCloud/dbauth-sdk-python',
    packages=find_packages(),
    install_requires=[
        "requests",
        'protobuf>=3.19.0',
        "pycryptodome~=3.20.0",
        "google>=3.0.0",
        "tencentcloud-sdk-python>=3.0.1224"
    ],
    python_requires=">=3.6",
    keywords=["DBAuth SDK", "OpenAPI SDK"],
    license="Apache License 2.0",
    include_package_data=True,
    project_urls={
        "Source": "https://github.com/TencentCloud/dbauth-sdk-python",
    },
)
