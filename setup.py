import setuptools
import img2epub


setuptools.setup(
    name="img2epub",
    version=img2epub.__version__,
    description="Generate EPUB book from image file set.",
    author="takatoh",
    author_email="takatoh.m@gmail.com",
    packages=setuptools.find_packages(),
    package_dir={"img2epub": "img2epub"},
    package_data={"img2epub": ["data/*"]},
    install_requires=[
        "jinja2"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts":[
            "img2epub=img2epub.command:main",
        ],
    }
)
