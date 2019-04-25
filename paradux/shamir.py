#!/usr/bin/python
#
# Implements Shamir Secret Sharing.
#
# Partially based on the public domain algorithm given here:
# https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

from __future__ import division
from __future__ import print_function
import random
import paradux.logging


# Maps the n-th Mersenne Prime to the N in its value 2**N-1
MERSENNE = [
    1, # not really a prime, but fills index=0
    2,
    3,
    5,
    7,                                                                  
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689 ]


def mersenneForBits(nbits):
    """
    Given the number of bits secrets are expected to be long, determine
    which Mersenne prime number is appropriate.

    :param nbits: the number of bits secrets are expected to be long
    """
    global MERSENNE

    ret = -1;
    for i in range(len(MERSENNE)):
        m = MERSENNE[i]
        if m>= nbits:
            ret = i
            break
    if ret < 0:
        raise ValueError( "nbits to large for this implementation" )

    return ret


class Share:
    """
    Collects all the information in one share that is distributed
    to one steward.
    """
    def __init__(self, x, y):
        """
        Constructor.

        :param x: the polynomial was evaluated at this x value
        :param y: the value of the polynomial at this x value
        """
        self.x     = x
        self.y = y


    def getX(self):
        return self.x


    def getY(self):
        return self.y


    def asString(self):
        """
        Create printable string for this share.

        :return: printable string
        """
        return( "Shamir secret share (x="
               + str( self.x )
               + "): "
               + str( self.y ))


class ShareGenerator:
    """
    Knows how to generate Shares.
    """
    def __init__(self, sss, polyK1, secret ):
        """
        Constructor.

        :param sss:    the ShamirSecretSharing instance that produced this instance
        :param polyK1  coefficients of the polynomial, from a[k] to a[1]
                       (not secret = a[0])
        :param secret  the secret = a[0]

        """
        self.sss    = sss
        self.polyK1 = polyK1
        self.secret = secret


    def obtainShare(self, x):
        """
        Create a Share for x value x

        x: the x value
        return: the Share object
        """
        prime = self.sss.prime

        value = 0
        for coeff in self.polyK1:
            value *= x
            value += coeff
            value %= prime
        value *= x
        value += self.secret
        value %= prime

        paradux.logging.trace('obtainShare:', x, value )
        return Share(x, value)


    def getPolyK1(self):
        """
        Return the coefficients of the polynomial, from a[k] to a[1]
        but not a[]0 = secret

        return: array of integer
        """
        return self.polyK1


    def getSecret(self):
        """
        Return the secret.

        return the secret
        """
        return self.secret


class ShamirSecretSharing :
    """
    Knows how to split a secret into shares, and how to reconstruct the
    secret from shares, using a Mersenne prime.
    """

    def __init__(self, mersenne):
        """
        Constructor.

        :param mersenne:       which Mersenne prime to use. E.g if this is 5,
                               the 5th Mersenne prime (7) to use
        :param nbits: the number of bits secrets are expected to be long
        """
        global MERSENNE

        self.mersenne = mersenne
        self.prime    = 2**MERSENNE[self.mersenne] - 1
        paradux.logging.trace( 'Created ShamirSecretSharing:', self.mersenne, self.prime )


    def createGenerator(self, secret, requiredShares):
        """
        Create a generator that knows how to create new shares based on a new
        random polynomial

        :param secret:         the secret to be split
        :param requiredShares: the number of shares required to reconstruct the secret (k)
        :return:               the ShareGenerator from which to obtain the shares
        """
        if secret >= self.prime:
            raise ValueError('Secret too large for the configured number of bits: ' + str(secret) + ' vs ' + str(self.prime) )

        # create random polynomial of rank requiredShares where poly[0] is the secret
        polyK1 = []
        for i in range( 1, requiredShares ):
            polyK1.append(random.SystemRandom().randint(0, self.prime))

        return ShareGenerator(self, polyK1, secret)


    def restoreGenerator(self, secret, polyK1):
        """
        Create a generator that knows how to create new shares based on an
        existing polynomial
        
        :param secret: the secret to be split
        :param polyK1: the polynomial to use
        :return:       the ShareGenerator from which to obtain the shares
        """
        if secret >= self.prime:
            raise ValueError('Secret too large for the configured number of bits: ' + str(secret) + ' vs ' + str(self.prime) )

        return ShareGenerator(self, polyK1, secret)
        

    def restore(self, shares):
        """
        Given a set of shares, restore the secret.
        
        :param shares: the shares from which to reconstruct the secret
        :return:       the reconstructed secret
        """
        def _product(vals):
            """
            Helper method: calculate product of inputs
            """
            accum = 1
            for v in vals:
                accum *= v
            return accum


        def _extended_gcd(a, b):
            '''
            Helper method: division in integers modulus p means finding the inverse
            of the denominator modulo p and then multiplying the numerator by this
            inverse (Note: inverse of A is B such that A*B % p == 1) this can
            be computed via extended Euclidean algorithm
            http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation
            '''
            x = 0
            last_x = 1
            y = 1
            last_y = 0
            while b != 0:
                quot = a // b
                a, b = b, a%b
                x, last_x = last_x - quot * x, x
                y, last_y = last_y - quot * y, y
            return last_x, last_y


        def _divmod(num, den, p):
            '''
            Helper method: compute num / den modulo prime p

            To explain what this means, the return value will be such that
            the following is true: den * _divmod(num, den, p) % p == num
            '''
            inv, _ = _extended_gcd(den, p)
            return num * inv


        def _lagrange_interpolate(x, x_s, y_s, p):
            """
            Helper method.
            Find the y-value for the given x, given n (x, y) points;
            k points will define a polynomial of up to kth order
            """

            k = len(x_s)
            nums = []  # avoid inexact division
            dens = []
            for i in range(k):
                others = list(x_s)
                cur = others.pop(i)
                nums.append( _product( x   - o for o in others))
                dens.append( _product( cur - o for o in others))
            den = _product(dens)
            num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p)
                       for i in range(k)])
            return (_divmod(num, den, p) + p) % p


        paradux.logging.trace( 'restore', lambda: ' / '.join( map( lambda s : s.asString(), shares )))

        # do some consistency checking
        kShares = len(shares)
        if kShares < 2:
            raise ValueError( "Need at least two shares to restore" )

        # sort so we can easily look for duplicate x values in the shares
        shares = sorted( shares, key=lambda s: s.x )

        x_s = len(shares) * [ None ];
        y_s = len(shares) * [ None ];

        lastX    = shares[0].x
        x_s[0]   = shares[0].x;
        y_s[0]   = shares[0].y;

        for i in range( 1, len( shares )):
            s = shares[i]
            if s.x == lastX: # can't be larger; we have sorted
                raise ValueError( 'x value used more than once: ' + s.x + ' vs ' + x )
            lastX = s.x

            x_s[i] = shares[i].x
            y_s[i] = shares[i].y

        return _lagrange_interpolate( 0, x_s, y_s, self.prime )
