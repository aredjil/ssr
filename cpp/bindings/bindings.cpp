#include <pybind11/pybind11.h>
#include <pybind11/stl.h>  // for std::vector, etc.
#include "ssr.hpp"

namespace py = pybind11;

PYBIND11_MODULE(pyssr, m) {
    m.doc() = "SSR simulation bindings";

    py::class_<ssr_t>(m, "ssr_t")
        .def_readwrite("duration", &ssr_t::duration)
        .def_readwrite("size", &ssr_t::size)
        .def_readwrite("visited_states", &ssr_t::visited_states);

    py::class_<SSR>(m, "SSR")
        .def(py::init<>())
        .def(py::init<const uint64_t &>())
        .def("ssr_std", &SSR::ssr_std)
        .def("ssr_noisy", &SSR::ssr_noisy)
        .def("ssr_casc", &SSR::ssr_casc);
}
