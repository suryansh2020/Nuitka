//
//     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
//
//     Part of "Nuitka", an optimizing Python compiler that is compatible and
//     integrates with CPython, but also works on its own.
//
//     If you submit Kay Hayen patches to this software in either form, you
//     automatically grant him a copyright assignment to the code, or in the
//     alternative a BSD license to the code, should your jurisdiction prevent
//     this. Obviously it won't affect code that comes to him indirectly or
//     code you don't submit to him.
//
//     This is to reserve my ability to re-license the code at a later time to
//     the PSF. With this version of Nuitka, using it for a Closed Source and
//     distributing the binary only is not allowed.
//
//     This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation, version 3 of the License.
//
//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.
//
//     You should have received a copy of the GNU General Public License
//     along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
//     Please leave the whole of this copyright notice intact.
//
#ifndef __NUITKA_COMPILED_FUNCTION_H__
#define __NUITKA_COMPILED_FUNCTION_H__

#include "Python.h"
#include "frameobject.h"

// Compiled function type.

// The backbone of the integration into CPython. Try to behave as well as normal functions
// and builtin functions, or even better.

// Cleanup function to be called when the function object is released.
typedef void (*releaser)( void * );

// Method argument parsing function.
typedef PyObject *(*method_arg_parser)( PyObject *, PyObject *, PyObject *, PyObject *);
typedef PyObject *(*function_arg_parser)(PyObject *, PyObject *, PyObject * );

typedef PyObject *(*argless_code)(PyObject *);

// The Nuitka_FunctionObject is the storage associated with a compiled function instance
// of which there can be many for each code.
typedef struct {
    PyObject_HEAD

    PyObject *m_name;

    void *m_context;
    releaser m_cleanup;

    PyObject *m_module;
    PyObject *m_doc;

    PyCodeObject *m_code_object;

    void *m_code;
    bool m_has_args;

    method_arg_parser m_method_arg_parser;

    PyObject *m_dict;
    PyObject *m_weakrefs;

    // List of defaults, for use in func_defaults and parameter parsing.
    PyObject *m_defaults;

    long m_counter;
} Nuitka_FunctionObject;

extern PyTypeObject Nuitka_Function_Type;


// Make a function without context.
extern PyObject *Nuitka_Function_New( function_arg_parser code, method_arg_parser, PyObject *name, PyCodeObject *code_object, PyObject *defaults, PyObject *module, PyObject *doc );

// Make a function with context.
extern PyObject *Nuitka_Function_New( function_arg_parser code, method_arg_parser, PyObject *name, PyCodeObject *code_object, PyObject *defaults, PyObject *module, PyObject *doc, void *context, releaser cleanup );

// Make a function that is only a yielder, no args.
extern PyObject *Nuitka_Function_New( argless_code code, PyObject *name, PyObject *module, PyObject *doc, void * );

static inline bool Nuitka_Function_Check( PyObject *object )
{
    return Py_TYPE( object ) == &Nuitka_Function_Type;
}

static inline PyObject *Nuitka_Function_GetName( PyObject *object )
{
    return ((Nuitka_FunctionObject *)object)->m_name;
}

#endif
