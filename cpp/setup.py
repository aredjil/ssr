    from setuptools import setup, Extension
    import pybind11
    from pybind11.setup_helpers import build_ext

    ext_modules = [
        Extension(
            "pyssr",
            sources=["bindings/bindings.cpp"],  # Remove ssr.cpp if header-only
            include_dirs=[
                pybind11.get_include(),
                pybind11.get_include(user=True),
                "./include"
            ],
            language="c++",
            extra_compile_args=["-O3", "-march=native", "-std=c++17", "-Wall", "-Wextra"],
        ),
    ]

    setup(
        name="pyssr",
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )
