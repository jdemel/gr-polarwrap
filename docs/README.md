# gr-polarwrap

This is the GNU Radio block wrapper for `polar-codes`. An awesome high-throughput, low-latency polar encoder/decoder implementation.

## Install dependencies

In order to build this module, first, install its dependencies

* [polar-codes](https://github.com/ant-uni-bremen/polar-codes), needs some extra love. Build with <br>`cmake -DCMAKE_INSTALL_PREFIX=[GNURADIO_INSTALL_PREFIX] ..`<br>

## Code formatting

This is the current way to format everything:

`find . -regex '.*\.\(c\|cc\|cpp\|cxx\|h\|hh\)' -not -path "*build*" -exec clang-format -style=file -i {} \;`
