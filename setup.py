import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wsb-sentiment",
    version="1.0.0",
    author="Joshua David Golafshan",
    description="Python-based API. Finds tickers on the subreddit of 'WallStreetBets'",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/JGolafshan/KenoAPI",
    keywords=["trading", "algo" "stock", "sentiment", "wallstreetbets"],
    packages=["app"],
    install_requires=[
        're',
        'os',
        'praw',
        'pandas',
        'datetime'
    ],
    package_dir=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)


"""
python setup.py sdist
python setup.py bdist_wheel

2: twine upload --skip-existing dist/*
"""