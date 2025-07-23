#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  
#include "ssr.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pyssr, m) {
    m.doc() = "SSR simulation bindings";

    py::class_<SSR>(m, "SSR")
        .def(py::init<>())
        .def("ssr_std", &SSR::ssr_std, py::arg("n_states"), 
        "Run the standard SSR\n\n"
        "Parameters:\n"
        "n_states   Number of states\n"
    )
        .def("ssr_noisy", &SSR::ssr_noisy, py::arg("n_states"), py::arg("lambda"), 
        "Run the noisy SSR\n\n"
        "Parameters:\n"
        "n_staes    Number of states\n"
        "lambda     Noisy ratio\n"

    )
        .def("ssr_casc", &SSR::ssr_casc, py::arg("n_states"), py::arg("mu"), 
        "Run the SSR with cascades\n\n"
        "Parameters:\n"
        "n_staes    Number of states\n"
        "mu         Multiplicative factor\n");
}
