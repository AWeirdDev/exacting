from setuptools import setup
from Cython.Build import cythonize

setup(
    name="python/exacting/",
    ext_modules=cythonize(
        [
            "python/exacting/result.py",
        ]
    ),
    package_dir={"": "python"},
)
