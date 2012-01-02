#
#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     If you submit Kay Hayen patches to this software in either form, you
#     automatically grant him a copyright assignment to the code, or in the
#     alternative a BSD license to the code, should your jurisdiction prevent
#     this. Obviously it won't affect code that comes to him indirectly or
#     code you don't submit to him.
#
#     This is to reserve my ability to re-license the code at a later time to
#     the PSF. With this version of Nuitka, using it for a Closed Source and
#     distributing the binary only is not allowed.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Please leave the whole of this copyright notice intact.
#
""" Module like __future__ for things that are no more in CPython3, but provide compatible fallbacks.

This is required to run the same code easily with both CPython2 and CPython3.
"""

# pylint: disable=W0622

# Work around for CPython 3.x renaming long to int.
try:
    long = long
except NameError:
    long = int

# Work around for CPython 3.x renaming unicode to str.
try:
    unicode = unicode
except NameError:
    unicode = str

# Work around for CPython 3.x removal of commands
try:
    import commands
except ImportError:
    # false alarm, no re-import, just another try if the above fails, which it will
    # on Python3 pylint: disable=W0404

    import subprocess as commands

try:
    import exceptions

    builtin_exception_names = [
        str( x ) for x in dir( exceptions )
        if x.endswith( "Error" ) or x in ( "StopIteration", "GeneratorExit" )
    ]

except ImportError:
    exceptions = {}

    import sys

    for x in dir( sys.modules[ "builtins" ] ):
        name = str( x )

        if name.endswith( "Error" ) or name in ( "StopIteration", "GeneratorExit" ):
            exceptions[ name ] = x

    builtin_exception_names = [
        key for key, value in exceptions.items()
    ]


assert "ValueError" in builtin_exception_names
assert "StopIteration" in builtin_exception_names

def iterItems( d ):
    try:
        return d.iteritems()
    except AttributeError:
        return d.items()


# For PyLint to be happy.
assert long
assert unicode
assert commands
assert exceptions
