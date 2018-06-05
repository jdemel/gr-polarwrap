/* -*- c++ -*- */

#define POLARWRAP_API

%include "gnuradio.i"			// the common stuff
%include "fec_swig.i"

//load generated python docstrings
%include "polarwrap_swig_doc.i"

%{
#include "polarwrap/encoderwrap.h"
#include "polarwrap/decoderwrap.h"
%}


%include "polarwrap/encoderwrap.h"
%include "polarwrap/decoderwrap.h"
