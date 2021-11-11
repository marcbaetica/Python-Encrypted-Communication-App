import unittest
import rsa
from hashlib import md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s, sha3_224, sha3_256, sha3_384, sha3_512, shake_128, shake_256
from cryptography.fernet import Fernet


class Encryption:
    @classmethod
    def hash(cls, string, function='sha256'):
        """Hashing function. Defaults to sha256 encryption.

        :param string: The message to hash.
        :param function: The cryptographic hash function. Defaults to 'sha256'.
                         Also supports md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s, sha3_224, sha3_256,
                         sha3_384, sha3_512, shake_128, shake_256
        :return: (string) Message digest in hexadecimal format.
        """
        return eval(function)(string.encode()).hexdigest()

    @classmethod
    def generate_symmetric_key(cls):
        return Fernet.generate_key()

    @classmethod
    def generate_asymmetric_keys(cls):
        public_key, private_key = rsa.newkeys(512)
        return public_key, private_key

    @classmethod
    def encrypt_message(cls, message, key, encryption_type):
        if encryption_type == 'symmetric':
            return Fernet(key).encrypt(message)
        if encryption_type == 'asymmetric':
            return rsa.encrypt(message, key)
        else:
            raise ValueError(f'Encryption type has to be either symmetric or asymmetric. Received: {encryption_type}')

    @classmethod
    def decrypt_message(cls, message, key, encryption_type):
        if encryption_type == 'symmetric':
            return Fernet(key).decrypt(message)
        if encryption_type == 'asymmetric':
            return rsa.decrypt(message, key)
        else:
            raise ValueError(f'Encryption type has to be either symmetric or asymmetric. Received: {encryption_type}')


class EncryptionTests(unittest.TestCase):
    def test_hashing_has_expected_char_size(self):
        pass  # TODO: Fill this in at a later time.

    def test_symmetric_encrypting_decrypting_output(self):
        messages = ['aaa', '111', '   ']
        symmetric_key = Encryption.generate_symmetric_key()
        for message in messages:
            encrypted_message = Encryption.encrypt_message(message.encode(), symmetric_key, 'symmetric')
            decrypted_message = Encryption.decrypt_message(encrypted_message, symmetric_key, 'symmetric')
            self.assertEqual(message, decrypted_message.decode())

    def test_asymmetric_encrypting_decrypting_output(self):
        messages = ['aaa', '111', '   ']
        public_key, private_key = Encryption.generate_asymmetric_keys()
        for message in messages:
            encrypted_message = Encryption.encrypt_message(message.encode(), public_key, 'asymmetric')
            decrypted_message = Encryption.decrypt_message(encrypted_message, private_key, 'asymmetric')
            self.assertEqual(message, decrypted_message.decode())


if __name__ == '__main__':
    unittest.main()
