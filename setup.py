from distutils.core import setup

from Cython.Build import cythonize
from Cython.Compiler import Options

# https://cython.readthedocs.io/en/latest/src/tutorial/cython_tutorial.html
#  python setup.py build_ext --inplace
# python setup.py build_ext --build-lib 'c_modules'
Options.annotate = True

setup(
    ext_modules=cythonize(["cython_constraint.pyx"], annotate=True)
)
