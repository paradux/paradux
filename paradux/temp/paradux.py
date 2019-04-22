#!/usr/bin/python
#
# The core Paradux functionality.
#
# Copyright (C) 2019 and later, Paradux project.
# All rights reserved. License: see package.
#

    






import ShamirSecretSharing from paradux.shamir

class Paradux:

    def __init__( self, key_size =  ):







from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from paradux.shamir_secret_sharing import ShamirSecretSharing;





    key_size = 120
    private_key = 112233

    print( "Secret: " + str( private_key ))

    sss = ShamirSecretSharing( key_size )
    shares = sss.split( private_key, 3, 6 )

    for s in shares:
        print( "Share: " + s.asString())

    restored_private_key = sss.restore( shares[ 1:4 ] )

#    restored_private_pem = private_key.private_bytes(
#       encoding=serialization.Encoding.PEM,
#       format=serialization.PrivateFormat.PKCS8,
#       encryption_algorithm=serialization.NoEncryption())

    print( "Restored: " + str( restored_private_key ))








from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateNumbers

from paradux.shamir import ShamirSecretSharing;






    # Generate a new key pair
    
    key_size = 4096

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend())

    print( "Have private key" );

    # Split the 

    ciphertext = public_key.encrypt(
        b"Hello, world",
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print( "Have ciphertext, now restoring private key" )

    private_numbers = private_key.private_numbers();
    public_numbers  = public_key.public_numbers()


    n = public_numbers.n
    e = public_numbers.e
    d = private_numbers.d

    ( p, q ) = rsa.rsa_recover_prime_factors( n, e, d )

    iqmp = rsa.rsa_crt_iqmp( p, q )
    dmp1 = rsa.rsa_crt_dmp1( d, p )
    dmq1 = rsa.rsa_crt_dmq1( d, q )


    private_numbers2 = RSAPrivateNumbers( p, q, d, dmp1, dmp1, iqmp, public_numbers )

    private_key2 = private_numbers2.private_key(backend=default_backend())

    plaintext = private_key2.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print( "Decrypted: " + str(plaintext) )

    # print( "Private key:" );
    # print( type( private_key ))
    # print( type( private_key.private_numbers() ))
    # print( private_key.private_numbers().p )
    # print( private_key.private_numbers().q )
    # print( private_key.private_numbers().d )

    # print( "Public key:" );
    # print( type( public_key ))
    # print( type( public_key.public_numbers() ))
    # print( public_key.public_numbers().n )
    # print( public_key.public_numbers().e )
    
    #_key_size => 4096
    # _rsa_cdata => <cdata 'RSA *' 0x55a4dfc275b0>

    #for k in dir(private_key):
    #    print( str(k) + " => " + str(getattr( private_key, k )))

    # print(vars(private_key))
    exit( 0 )

    private_pem = private_key.private_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PrivateFormat.PKCS8,
       encryption_algorithm=serialization.NoEncryption())

    print( private_pem )
    exit( 0 )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo )

    print( "Private key:\n" )
    print( private_pem );

    print( "Public key:\n" )
    print( public_pem );


    sss = ShamirSecretSharing( key_size )
    shares = sss.split( private_key, 3, 5 )

    for s in shares:
        print( "Share: " + s.asString())

    restored_private_key = sss.restore( shares )

#    restored_private_pem = private_key.private_bytes(
#       encoding=serialization.Encoding.PEM,
#       format=serialization.PrivateFormat.PKCS8,
#       encryption_algorithm=serialization.NoEncryption())

    print( "Restored: " + restored_private_key )

    
