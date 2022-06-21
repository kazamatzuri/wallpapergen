from setuptools import setup

setup(
    name="WPGen",
    description="Yet another wallpaper generator",
    url="https://github.com/kazamatzuri/wallpapergen",
    author="Fabian",
    author_email="fabian@fabianhaupt.de",
    license="MIT",
    packages=["wpgen"],
    entry_points={"console_scripts": ["wpgen=wpgen.command_line:main"]},
    test_suite="nose.collector",
    tests_require=["nose"],
    install_requires=[
        "pytz==2018.5",
        "numpy==1.22.0",
        "pandas==0.23.4",
        "gitchangelog>=3.0.4",
        "pre-commit>=1.14.4",
        "black>=18.9b0",
        "pystache>=0.5.4",
        "Pillow>=6.0.0",
        "geomdl>=5.2.1",
        "numba>=0.43.1"
    ],
    version="1.0.0",
    zip_safe=False,
)
