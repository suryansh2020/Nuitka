#!/usr/bin/env python
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

from __future__ import print_function

import os, sys, tempfile, subprocess

# Go its own directory, to have it easy with path knowledge.
os.chdir( os.path.dirname( os.path.abspath( __file__ ) ) )
os.chdir( ".." )

path_sep = ";" if "win" in sys.platform else ":"

# Add the local bin directory to search path start.
os.environ[ "PATH" ] = os.path.join( os.getcwd(), "bin" ) + path_sep + os.environ[ "PATH" ]


def checkExecutableCommand( command ):
    path = os.environ[ "PATH" ]

    suffixes = ( ".exe", ) if "win" in sys.platform else ( "", )

    for part in path.split( path_sep ):
        if not part:
            continue

        for suffix in suffixes:
            if os.path.exists( os.path.join( part, command + suffix ) ):
                return True
    else:
        return False

def setExtraFlags( where, name, flags ):
    where = os.path.join( tempfile.gettempdir(), name, where )

    if not os.path.exists( where ):
        os.makedirs( where )

    os.environ[ "NUITKA_EXTRA_OPTIONS" ] = flags + " --output-dir=" + where

def executeSubTest( command ):
    parts = command.split()

    parts[0] = parts[0].replace( "/", os.path.sep )

    if parts[0].endswith( ".py" ) and "win" in sys.platform:
        parts.insert( 0, r"C:\Python27\python.exe" )

    command = " ".join( parts )

    print(command, os.getcwd())


    result = subprocess.call( command, shell = True )

    if result != 0:
        sys.exit( result )

def execute_tests( where, use_python, flags ):
    print("Executing test case called %s with CPython %s and extra flags '%s'." % (
        where,
        use_python,
        flags
    ))

    if "win" in sys.platform:
        if use_python == "python2.6":
            os.environ[ "PYTHON" ] = r"C:\Python26\python.exe"
        elif use_python == "python2.7":
            os.environ[ "PYTHON" ] = r"C:\Python27\python.exe"
        else:
            assert False, use_python
    else:
        os.environ[ "PYTHON" ] = use_python

    print("Running the basic tests with options '%s' with %s:"  % ( flags, use_python ))
    setExtraFlags( where, "basics", flags )
    executeSubTest( "./tests/basics/run_all.py search" )

    print("Running the syntax tests with options '%s' with %s:"  % ( flags, use_python ))
    setExtraFlags( where, "syntax", flags )
    executeSubTest( "./tests/syntax/run_all.py search" )

    print("Running the program tests with options '%s' with %s:" % ( flags, use_python ))
    setExtraFlags( where, "programs", flags )
    executeSubTest( "./tests/programs/run_all.py search" )

    print("Running the CPython 2.6 tests with options '%s' with %s:" % ( flags, use_python ))

    setExtraFlags( where, "26tests", flags )
    executeSubTest( "./tests/CPython/run_all.py search" )

    # Running the Python 2.7 test suite with CPython 2.6 gives little insight, because
    # "importlib" will not be there and that's it.
    if use_python != "python2.6":
        setExtraFlags( where, "27tests", flags )
        executeSubTest( "./tests/CPython27/run_all.py search" )

        print("Running the CPython 2.7 tests with options '%s' with %s:" % ( flags, use_python ))
        executeSubTest( "./tests/CPython27/run_all.py search" )

    del os.environ[ "NUITKA_EXTRA_OPTIONS" ]


if checkExecutableCommand( "python3.2" ):
    executeSubTest( "python3.2 bin/Nuitka.py --version 2>/dev/null" )
else:
    print("Cannot execute Python 3.2 tests, not installed.")

execute_tests( "python2.6-debug", "python2.6", "--debug" )
execute_tests( "python2.7-debug", "python2.7", "--debug" )

execute_tests( "python2.6-nodebug", "python2.6", "" )
execute_tests( "python2.7-nodebug", "python2.7", "" )

del os.environ[ "PYTHON" ]

print("Running the reflection test in debug mode with default python:")
executeSubTest( "./tests/reflected/compile_itself.py search" )

print("OK.")
