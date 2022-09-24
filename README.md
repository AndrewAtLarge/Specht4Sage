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

By default, the wrapper assumes that the gap3 executable is '/usr/local/bin/gap'.
This can be overridden using the optional gap argument:

    sage: H=Specht(4, gap='/some/other/place')
    
Examples
--------

```python
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
```

AUTHOR:
- Andrew Mathas (2015): initial version
