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

class ShamirSecretSharing :
    """
    Knows how to split a secret into shares, and how to reconstruct the
    secret from shares, using a Mersenne prime.
    """

    class Share:
        """
        Collects all the information in one share that is distributed
        to one steward.
        """
        def __init__( self, mersenne, x, requiredShares, share ):
            """
            Constructor.

            :param mersenne:       which Mersenne prime was used. E.g if this is 5,
                                   the 5th Mersenne prime (7) was used
            :param x:              the polynomial was evaluated at this x value
            :param requiredShares: the number of shares required so the secret
                                   can be reconstructed
            :param share           the value of the share
            """
            self.mersenne       = mersenne
            self.x              = x
            self.requiredShares = requiredShares
            self.share          = share

        def asString( self ):
            """
            Create printable string for this share.

            :return: printable string
            """
            return( "Shamir secret share (x="
                   + str( self.x )
                   + ", "
                   + str( self.requiredShares )
                   + " shares needed, using the "
                   + str( self.mersenne )
                   + "th Mersenne prime): "
                   + str( self.share ))

    # Maps the n-th Mersenne Prime to the N in its value 2**N-1
    MERSENNE = [
        1, # not really a prime, but fills index0
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
        
    def __init__( self, nbits ):
        """
        Constructor.

        :param nbits: the number of bits secrets are expected to be long
        """

        self.nbits    = nbits;

        # find an appropriate Mersenne prime
        self.mersenne = -1;
        for i in range( len( ShamirSecretSharing.MERSENNE )):
            m = ShamirSecretSharing.MERSENNE[i]
            if m>= nbits:
                self.mersenne = i
                break
        if self.mersenne < 0:
            raise ValueError( "nbits to large for this implementation" )

        self.prime = 2**ShamirSecretSharing.MERSENNE[self.mersenne] - 1

    def split( self, secret, requiredShares, nShares ):
        """
        Split a secret into n shares, where k are required to reconstruct

        :param secret:         the secret to be split
        :param requiredShares: the number of shares required to reconstruct the secret (k)
        :param nShares:        the number of shares to create (n)
        :return:               the n Share objects that constitute the split secret
        """

        if secret >= self.prime:
            raise ValueError( 'Secret too large for the configured number of bits: ' + str( secret ) + ' vs ' + str( self.prime ) )
        if requiredShares > nShares:
            raise ValueError( 'Cannot require more shares to reconstruct than created shares' )

        # create random polynomial of rank requiredShares where poly[0] is the secret
        poly = requiredShares * [ None ]
        poly[0] = secret
        for i in range( 1, requiredShares ):
            poly[i] = random.SystemRandom().randint( 0, self.prime )

        # calculate poly(1...nShares+1) and create Share objects
        shares = nShares * [None]

        for x in range( 1, nShares+1 ):
            value = 0
            for coeff in reversed(poly):
                value *= x
                value += coeff
                value %= self.prime

            shares[x-1] = ShamirSecretSharing.Share( self.mersenne, x, requiredShares, value )

        return shares

    def restore( self, shares ):
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

        # do some consistency checking
        kShares = len(shares)
        if kShares < 2:
            raise ValueError( "Need at least two shares to restore" )

        # sort so we can easily look for duplicate x values in the shares
        shares = sorted( shares, key=lambda s: s.x )

        x_s = len(shares) * [ None ];
        y_s = len(shares) * [ None ];

        mersenne = shares[0].mersenne
        lastX    = shares[0].x
        x_s[0]   = shares[0].x;
        y_s[0]   = shares[0].share;

        if kShares != shares[0].requiredShares :
            raise ValueError( 'Number of provided shares is not number of required shares: ' + str(kShares) + ' vs ' + str(shares[0].requiredShares ))

        for i in range( 1, len( shares )):
            s = shares[i]
            if s.mersenne != mersenne:
                raise ValueError( 'Not the same Mersenne prime used in the shares: ' + s.mersenne + ' vs ' + mersenne )
            if s.x == lastX: # can't be larger; we have sorted
                raise ValueError( 'x value used more than once: ' + s.x + ' vs ' + x )
            if s.requiredShares != kShares:
                raise ValueError( 'Number of provided shares is not number of required shares: ' + str(kShares) + ' vs ' + str(s.requiredShares ))
            lastX = s.x

            x_s[i] = shares[i].x
            y_s[i] = shares[i].share

        prime = 2**ShamirSecretSharing.MERSENNE[mersenne] - 1
        return _lagrange_interpolate( 0, x_s, y_s, prime )
