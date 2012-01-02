#
#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Python test originally created or extracted from other peoples work. The
#     parts and resulting tests are too small to be protected and therefore
#     is in the public domain.
#
#     If you submit Kay Hayen patches to this in either form, you automatically
#     grant him a copyright assignment to the code, or in the alternative a BSD
#     license to the code, should your jurisdiction prevent this. Obviously it
#     won't affect code that comes to him indirectly or code you don't submit to
#     him.
#
#     This is to reserve my ability to re-license the official code at any time,
#     to put it into public domain or under PSF.
#
#     Please leave the whole of this copyright notice intact.
#



def simple_comparisons( x, y ):
    if 'a' <= x <= y <= 'z':
        print "One"

    if 'a' <= x <= 'z':
        print "Two"

    if 'a' <= x > 'z':
        print "Three"

print "Simple comparisons:"

simple_comparisons( "c", "d" )

def side_effect():
    print "<side_effect>"

    return 7

def side_effect_comparisons():
    print "Should have side effect:"

    print 1 < side_effect() < 9

    print "Should not have side effect due to short circuit"

    print 3 < 2 < side_effect() < 9

print "Check for expected side effects only:"

side_effect_comparisons()

def function_torture_is():
    a = ( 1, 2, 3 )

    for x in a:
        for y in a:
            for z in a:
                print x, y, z, ":", x is y is z, x is not y is not z

function_torture_is()

print "Check if lambda can have expression chains:"

def function_lambda_with_chain():

    a = ( 1, 2, 3 )

    x = lambda x : x[0] < x[1] < x[2]

    print x(a)

function_lambda_with_chain()

def generator_function_with_chain():
    x = ( 1, 2, 3 )

    yield x[0] < x[1] < x[2]

print list( generator_function_with_chain() )

def contraction_with_chain():
    return [ x[0] < x[1] < x[2] for x in [ ( 1, 2, 3 ) ] ]

print contraction_with_chain()

def genexpr_with_chain():
    return ( x[0] < x[1] < x[2] for x in [ ( 1, 2, 3 ) ] )

print list( genexpr_with_chain() )

class class_with_chain:
    x = ( 1, 2, 3 )
    print x[0] < x[1] < x[2]

x = ( 1, 2, 3 )
print x[0] < x[1] < x[2]

class CustomOps( int ):
    def __lt__( self, other ):
        print "<", self, other

        return True

    def __gt__( self, other ):
        print ">", self, other

        return False


print "Custom ops, to enforce chain eval order and short circuit:"
CustomOps( 7 ) < CustomOps( 8 ) > CustomOps( 6 )

print "Custom ops, do short circuit:"
CustomOps( 8 ) > CustomOps( 7 ) < CustomOps( 6 )

def inOperatorChain():
    print "In operator chains:"
    print 3 in [3,4] in [[3,4]]
    print 3 in [3,4] not in [[3,4]]

    if 3 in [3,4] in [[3,4]]:
       print "Yes"
    else:
       print "No"

    if 3 in [3,4] not in [[3,4]]:
       print "Yes"
    else:
       print "No"


inOperatorChain()
