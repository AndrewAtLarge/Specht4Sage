r"""
Very rudimentary wrapper class for accessing parts of the gap3 Specht package.
Currently only gives access to (graded) decomposition numbers and (graded)
decomposition matrices. May expand in the future, or on demand.

For this code to work you need to have gap3 installed on your system together
with the sage interface to gap3 (I have forgotten who wrote this and if you need
to do anything special to install this) and you need a reasonably up-to-date
version of the Specht package.

    sage: H=Specht(3)  # Hecke algebras at a third root of unity (e-3)
    sage: H.graded_decomposition_number([2,2,2],[6])
    v^2

By default, the wrapped assumes that the gap3 executable is '/usr/local/bin/gap'.
This can be overridden using the optional gap argument:

    sage: H=Specht(4, gap='/some/other/place')

AUTHOR:
- Andrew Mathas (2015): initial version

"""

class Specht(object):
    r"""
    Very rudimentary wrapper class for accessing parts of the gap3 Specht package.

    INPUTS:

    - ``e``   -- the quantum characteristic of the Hecke algebras being considered

    - ``p``   -- the characteristic of the Hecke algebras being considered (default 0)

    - ``gap`` -- the location of the gap3 executable (defaults to `/usr/local/bin/gap`)

    - ``v``   -- the indeterminate used for the graded decomposition numbers

    EXAMPLES::

        sage: R.<q>=LaurentPolynomialRing(QQ)
        sage: H=Specht(3,v=q)
        sage: H.graded_decomposition_number([2,2,2],[6])
        q^2
        sage: H.graded_decomposition_matrix(6)
        6      |   1
        5,1    |   v     1
        4,2    |   .     .     1
        4,1^2  |   .     v     .     1
        3^2    |   .     v     .     .     1
        3,2,1  |   v   v^2     .     v     v     1
        3,1^3  |   .     .     .   v^2     .     v
        2^3    | v^2     .     .     .     .     v
        2^2,1^2|   .     .     .     .     .     .     1
        2,1^4  |   .     .     .     .     v   v^2     .
        1^6    |   .     .     .     .   v^2     .     .
        sage: H.decomposition_matrix(6)
        6      | 1
        5,1    | 1 1
        4,2    | . . 1
        4,1^2  | . 1 . 1
        3^2    | . 1 . . 1
        3,2,1  | 1 1 . 1 1 1
        3,1^3  | . . . 1 . 1
        2^3    | 1 . . . . 1
        2^2,1^2| . . . . . . 1
        2,1^4  | . . . . 1 1 .
        1^6    | . . . . 1 . .
    """
    def __init__(self, e, p=0, gap='/usr/local/bin/gap', v=None):
        self._gap=Gap3(command=gap)
        self._gap.RequirePackage('"specht"')
        self._e=e
        self._p=p
        if self._p>0:
            self._hecke=self._gap.Specht(self._e, self._p)
        else:
            self._hecke=self._gap.Specht(self._e)

        if v is None:
            self._laurent=LaurentPolynomialRing(IntegerRing(),'v')
            self._v=self._laurent.gen()
        else:
            self._v=v
            self._laurent=self._v.parent()

    def __repr__(self):
        r"""
        Return a string representation of the Hecke algebra record.

        EXAMPLES::

            sage: H=Specht(3,v=q); H
            Hecke(e=3, p=0)
        """
        return 'Hecke(e=%s, p=%s)' % (self._e, self._p)

    def decomposition_matrix(self, n):
        r"""
        Return the decomposition matrix for the Hecke algebra `H_n`.

        The decompositions matrix is returned as a Gap object. It displays
        correctly and some it its functionality is available but it is not a
        sage object.

        EXAMPLES::

            aage: H=Specht(3)
            sage: H.decomposition_matrix(4)
            4    | 1
            3,1  | 1 1
            2^2  | . 1
            2,1^2| 1 1
            1^4  | 1 .
        """
        return self._gap.DecompositionMatrix(self._hecke,n)


    def decomposition_number(self, mu,nu):
        r"""
        Return the decomposition multiplicity, an integer, of the simple 
        module D(nu)` in the Specht module `S(mu)`.

        EXAMPLES::

            aage: H=Specht(3)
            sage: H.decomposition_number([5,1],[6])
            1
            sage: H.decomposition_number([4,2],[6])
            0
            sage: H=Specht(2)
            sage: H.decomposition_number([6,4,3,2,2,1], [8,6,4])
            5
            sage: H.decomposition_number(Partition([6,4,3,2,2,1]), [8,6,4])
            5
        """
        return Integer(self._gap.DecompositionNumber(self._hecke, mu,nu))

    def graded_decomposition_matrix(self, n):
        r"""
        Return the graded decomposition matrix for the Hecke algebra `H_n`.

        The decompositions matrix is returned as a Gap object. It displays
        correctly and some it its functionality is available but it is not a
        sage object.

        EXAMPLES::

            aage: H=Specht(3)
            sage: H.graded_decomposition_matrix(4)
            4    |   1
            3,1  |   v     1
            2^2  |   .     v
            2,1^2|   v   v^2
            1^4  | v^2     .
        
        """
        return self._gap.CrystalizedDecompositionMatrix(self._hecke,n)

    
    def __to_sage_polynomial(self, p):
        r"""
        Convert the gap (Laurent) polynomial `p` to a sage polynomial.

        EXAMPLES::

            sage: H=Specht(2)
            sage: H.graded_decomposition_number([6,4,3,2,2,1], [8,6,4])
            v^7 + 3*v^5 + v^3

        """
        return self._laurent.sum(int(p.coefficients[c+1])*self._v**(c+p.valuation) for c in range(len(p.coefficients)))

    def graded_decomposition_number(self, mu,nu):
        r"""
        Return the decomposition multiplicity, a Laurent polynomial in `v`, of the simple 
        module D(mu)` in the Specht module `S(nu)`.

        EXAMPLES::

            sage: H=Specht(2)
            sage: H.graded_decomposition_number([6,4,3,2,2,1], [8,6,4])
            v^7 + 3*v^5 + v^3
            sage: H.graded_decomposition_number(Partition([6,4,3,2,2,1]), [8,6,4])
            v^3 + 3*v^5 + v^7
            sage: [H.graded_decomposition_number(mu,[6]) for mu in Partitions(6)]
            [1, v, 0, v, 0, 0, v^2, 0, 0, v^2, v^3]
        """
        if self._p>0:
            raise NotImplementedError('graded decomposition numbers are only known in characteristic zero')
        
        Pq=self._hecke.Pq(nu)
        try:
            dmunu=Pq.coeffs[Pq.elts.Position(mu)]
        except TypeError:
            # this happens only S(mu) does not appear in P(nu) so the multiplicity is zero
            return 0
        # dmunu is now a gap3 polynomial, so convert to a sage polynomial in v
        return self.__to_sage_polynomial(dmunu)



