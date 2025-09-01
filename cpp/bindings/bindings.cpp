#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>  // for NumPy support
#include "ssr.hpp"

namespace py = pybind11;

// Helper to convert std::vector<int> → NumPy array
py::array_t<int> vector_to_numpy(const std::vector<int>& vec) {
    // Create Python-owned copy (NumPy array owns its memory)
    return py::array_t<int>(vec.size(), vec.data());
}

PYBIND11_MODULE(pyssr, m) {
    m.doc() = "SSR simulation bindings";

    // Base class with NumPy array return
    py::class_<ISSR, std::shared_ptr<ISSR>>(m, "ISSR")
        .def("run", [](ISSR &self, bool verbose) {
            std::vector<int> result = self.run(verbose);
            return vector_to_numpy(result);
        }, py::arg("verbose") = false);

    // Derived classes
    py::class_<STDSSR, ISSR, std::shared_ptr<STDSSR>>(m, "STDSSR")
        .def(py::init<int>());

    py::class_<NoisySSR, ISSR, std::shared_ptr<NoisySSR>>(m, "NoisySSR")
        .def(py::init<int, float>());

    py::class_<CascadeSSR, ISSR, std::shared_ptr<CascadeSSR>>(m, "CascadeSSR")
        .def(py::init<int, float>());
}
