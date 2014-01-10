"""
Elements of Arithmetic Subgroups
"""

################################################################################
#
#       Copyright (C) 2009, The Sage Group -- http://www.sagemath.org/
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#
################################################################################

from sage.structure.element cimport MultiplicativeGroupElement, MonoidElement, Element
from sage.rings.all import ZZ
import sage.matrix.all as matrix
from sage.matrix.matrix_integer_2x2 import Matrix_integer_2x2 as mi2x2

M2Z = matrix.MatrixSpace(ZZ,2)

cdef class ArithmeticSubgroupElement(MultiplicativeGroupElement):
    r"""
    An element of the group `{\rm SL}_2(\ZZ)`, i.e. a 2x2 integer matrix of
    determinant 1.
    """

    cdef object __x

    def __init__(self, parent, x, check=True):
        """
        Create an element of an arithmetic subgroup.

        INPUT:

        - parent - an arithmetic subgroup

        - x - data defining a 2x2 matrix over ZZ
          which lives in parent

        - check - if True, check that parent
          is an arithmetic subgroup, and that
          x defines a matrix of determinant 1.

        We tend not to create elements of arithmetic subgroups that aren't
        SL2Z, in order to avoid coercion issues (that is, the other arithmetic
        subgroups are "facade parents").

        EXAMPLES::

            sage: G = Gamma0(27)
            sage: sage.modular.arithgroup.arithgroup_element.ArithmeticSubgroupElement(G, [4,1,27,7])
            [ 4  1]
            [27  7]
            sage: sage.modular.arithgroup.arithgroup_element.ArithmeticSubgroupElement(Integers(3), [4,1,27,7])
            Traceback (most recent call last):
            ...
            TypeError: parent (= Ring of integers modulo 3) must be an arithmetic subgroup
            sage: sage.modular.arithgroup.arithgroup_element.ArithmeticSubgroupElement(G, [2,0,0,2])
            Traceback (most recent call last):
            ...
            TypeError: matrix must have determinant 1
            sage: sage.modular.arithgroup.arithgroup_element.ArithmeticSubgroupElement(G, [2,0,0,2], check=False)
            [2 0]
            [0 2]
            sage: x = Gamma0(11)([2,1,11,6])
            sage: TestSuite(x).run()

            sage: x = Gamma0(5).0
            sage: SL2Z(x)
            [1 1]
            [0 1]
            sage: x in SL2Z
            True
        """
        if check:
            from all import is_ArithmeticSubgroup
            if not is_ArithmeticSubgroup(parent):
                raise TypeError, "parent (= %s) must be an arithmetic subgroup"%parent

            x = mi2x2(M2Z, x, copy=True, coerce=True)
            if x.determinant() != 1:
                raise TypeError, "matrix must have determinant 1"
        else:
            x = mi2x2(M2Z, x, copy=True, coerce=False)
            # Getting rid of this would result in a small speed gain for
            # arithmetic operations, but it would have the disadvantage of
            # causing strange and opaque errors when inappropriate data types
            # are used with "check=False".

        x.set_immutable()
        MultiplicativeGroupElement.__init__(self, parent)
        self.__x = x

    def __setstate__(self, state):
        r"""
        For unpickling objects pickled with the old ArithmeticSubgroupElement class.

        EXAMPLE::

            sage: si = unpickle_newobj(sage.modular.arithgroup.arithgroup_element.ArithmeticSubgroupElement, ())
            sage: x = sage.matrix.matrix_integer_2x2.Matrix_integer_2x2(MatrixSpace(ZZ, 2), [1,1,0,1], copy=True, coerce=True)
            sage: unpickle_build(si, (Gamma0(13), {'_ArithmeticSubgroupElement__x': x}))
        """
        from all import SL2Z
        oldparent, kwdict = state
        self._set_parent(SL2Z)
        if kwdict.has_key('_ArithmeticSubgroupElement__x'):
            self.__x = kwdict['_ArithmeticSubgroupElement__x']
        elif kwdict.has_key('_CongruenceSubgroupElement__x'):
            self.__x = kwdict['_CongruenceSubgroupElement__x']
        else:
            raise ValueError, "Don't know how to unpickle %s" % repr(state)

    def __iter__(self):
        """
        EXAMPLES::

            sage: Gamma0(2).0
            [1 1]
            [0 1]
            sage: list(Gamma0(2).0)
            [1, 1, 0, 1]
        """
        return iter(self.__x)

    def __repr__(self):
        """
        Return the string representation of self.

        EXAMPLES::

            sage: Gamma1(5)([6,1,5,1]).__repr__()
            '[6 1]\n[5 1]'
        """
        return "%s"%self.__x

    def _latex_(self):
        """
        Return latex representation of self.

        EXAMPLES::

            sage: Gamma1(5)([6,1,5,1])._latex_()
            '\\left(\\begin{array}{rr}\n6 & 1 \\\\\n5 & 1\n\\end{array}\\right)'
        """
        return '%s' % self.__x._latex_()
        
    def __richcmp__(left, right, int op):
        r"""
        Rich comparison.

        EXAMPLE::

            sage: SL2Z.0 > None
            True
        """
        return (<Element>left)._richcmp(right, op)

    cdef int _cmp_c_impl(self, Element right_r) except -2:
        """
        Compare self to right, where right is guaranteed to have the same
        parent as self.

        EXAMPLES::

            sage: x = Gamma0(18)([19,1,18,1])
            sage: cmp(x, 3) is not 0
            True
            sage: cmp(x, x)
            0

            sage: x = Gamma0(5)([1,1,0,1])
            sage: x == 0
            False

        This once caused a segfault (see trac #5443)::

            sage: r,s,t,u,v = map(SL2Z, [[1, 1, 0, 1], [-1, 0, 0, -1], [1, -1, 0, 1], [1, -1, 2, -1], [-1, 1, -2, 1]])
            sage: v == s*u
            True
            sage: s*u == v
            True
        """
        cdef ArithmeticSubgroupElement right = <ArithmeticSubgroupElement>right_r
        return cmp(self.__x, right.__x)

    def __nonzero__(self):
        """
        Return True, since the self lives in SL(2,\Z), which does not
        contain the zero matrix.

        EXAMPLES::

            sage: x = Gamma0(5)([1,1,0,1])
            sage: x.__nonzero__()
            True
        """
        return True

    cpdef MonoidElement _mul_(self, MonoidElement right):
        """
        Return self * right.

        EXAMPLES::

            sage: x = Gamma0(7)([1,0,7,1]) * Gamma0(7)([3,2,7,5]) ; x # indirect doctest
            [ 3  2]
            [28 19]
            sage: x.parent()
            Modular Group SL(2,Z)

        We check that #5048 is fixed::

            sage: a = Gamma0(10).1 * Gamma0(5).2; a # random
            sage: a.parent()
            Modular Group SL(2,Z)

        """
        return self.__class__(self.parent(), self.__x * (<ArithmeticSubgroupElement> right).__x, check=False)

    def __invert__(self):
        """
        Return the inverse of self.

        EXAMPLES::

            sage: Gamma0(11)([1,-1,0,1]).__invert__()
            [1 1]
            [0 1]
        """
        I = mi2x2(M2Z, [self.__x[1,1], -self.__x[0,1], -self.__x[1,0], self.__x[0,0]], copy=True, coerce=True)
        return self.parent()(I, check=False)

    def matrix(self):
        """
        Return the matrix corresponding to self.

        EXAMPLES::

            sage: x = Gamma1(3)([4,5,3,4]) ; x
            [4 5]
            [3 4]
            sage: x.matrix()
            [4 5]
            [3 4]
            sage: type(x.matrix())
            <type 'sage.matrix.matrix_integer_2x2.Matrix_integer_2x2'>
        """
        return self.__x

    def determinant(self):
        """
        Return the determinant of self, which is always 1.

        EXAMPLES::

            sage: Gamma0(691)([1,0,691,1]).determinant()
            1
        """
        return ZZ(1)

    def det(self):
        """
        Return the determinant of self, which is always 1.

        EXAMPLES::

            sage: Gamma1(11)([12,11,-11,-10]).det()
            1
        """
        return self.determinant()

    def a(self):
        """
        Return the upper left entry of self.

        EXAMPLES::

            sage: Gamma0(13)([7,1,13,2]).a()
            7
        """
        return self.__x[0,0]

    def b(self):
        """
        Return the upper right entry of self.

        EXAMPLES::

            sage: Gamma0(13)([7,1,13,2]).b()
            1
        """
        return self.__x[0,1]

    def c(self):
        """
        Return the lower left entry of self.

        EXAMPLES::

            sage: Gamma0(13)([7,1,13,2]).c()
            13
        """
        return self.__x[1,0]

    def d(self):
        """
        Return the lower right entry of self.

        EXAMPLES::

            sage: Gamma0(13)([7,1,13,2]).d()
            2
        """
        return self.__x[1,1]

    def acton(self, z):
        """
        Return the result of the action of self on z as a fractional linear
        transformation.

        EXAMPLES::

            sage: G = Gamma0(15)
            sage: g = G([1, 2, 15, 31])

        An example of g acting on a symbolic variable::

            sage: z = var('z')
            sage: g.acton(z)
            (z + 2)/(15*z + 31)

        An example involving the Gaussian numbers::

            sage: K.<i> = NumberField(x^2 + 1)
            sage: g.acton(i)
            1/1186*i + 77/1186

        An example with complex numbers::

            sage: C.<i> = ComplexField()
            sage: g.acton(i)
            0.0649241146711636 + 0.000843170320404721*I

        An example with the cusp infinity::

            sage: g.acton(infinity)
            1/15

        An example which maps a finite cusp to infinity::

            sage: g.acton(-31/15)
            +Infinity
        """
        from sage.rings.infinity import is_Infinite, infinity
        if is_Infinite(z):
            if self.__x[1,0] != 0:
                return self.__x[0,0]/self.__x[1,0]
            else:
                return infinity
        if hasattr(z, 'denominator') and hasattr(z, 'numerator'):
            p, q = z.numerator(), z.denominator()
            P = self.__x[0,0]*p+self.__x[0,1]*q
            Q = self.__x[1,0]*p+self.__x[1,1]*q
            if Q == 0 and P != 0: 
                return infinity
            else:
                return P/Q
        return (self.__x[0,0]*z + self.__x[0,1])/(self.__x[1,0]*z + self.__x[1,1])

    def __getitem__(self, q):
        r"""
        Fetch entries by direct indexing.

        EXAMPLE::
            sage: SL2Z([3,2,1,1])[0,0]
            3
        """
        return self.__x[q]

    def __hash__(self):
        r"""
        Return a hash value.

        EXAMPLE::

            sage: hash(SL2Z.0)
            -4
        """
        return hash(self.__x)

    def __reduce__(self):
        r"""
        Used for pickling.

        EXAMPLE::

            sage: (SL2Z.1).__reduce__()
            (Modular Group SL(2,Z), ([1 1]
            [0 1],))
        """
        from all import SL2Z
        return SL2Z, (self.__x,)
