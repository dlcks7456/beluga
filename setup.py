from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="beluga",
    version="0.1.0",
    author="Chuck (Chan.Lee)",
    author_email="dlcks7456@kakao.com",
    description="설문 문항을 생성하고 관리하는 Python 라이브러리",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dlcks7456/beluga",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "beluga=beluga.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)