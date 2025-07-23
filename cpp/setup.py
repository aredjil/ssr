from setuptools import setup, Extension
import pybind11
from pybind11.setup_helpers import build_ext

ext_modules = [
    Extension(
        "pyssr",
        sources=["bindings/bindings.cpp", "./src/ssr.cpp"],
        include_dirs=[pybind11.get_include(), "include"],
        language="c++",
        extra_compile_args=["-O3", "-march=native", "-std=c++17"],  
    ),
]

setup(
    name="pyssr",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
