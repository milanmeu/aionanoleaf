from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aionanoleaf",
    version="0.0.1",
    author="Milan Meulemans",
    author_email="milan.meulemans@live.be",
    description="Async Python package for the Nanoleaf API",
    keywords="nanoleaf api canvas shapes elements light panels",
    license="LGPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/milanmeu/aionanoleaf",
    project_urls={
        "Say Thanks!": "https://saythanks.io/to/milan.meulemans@live.be",
        "Bug Tracker": "https://github.com/milanmeu/aionanoleaf/issues",
        "Source Code": "https://github.com/milanmeu/aionanoleaf",
        "Documentation": "https://github.com/milanmeu/aionanoleaf/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Home Automation",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    packages=["aionanoleaf"],
    package_data={"aionanoleaf": ["py.typed"]},
)
