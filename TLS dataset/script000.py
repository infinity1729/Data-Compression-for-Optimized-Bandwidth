from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime

def generate_certificate():
    # Generate a private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Generate a certificate signing request (CSR)
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"MyOrganization"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
    ])

    csr = x509.CertificateSigningRequestBuilder().subject_name(subject).sign(private_key, SHA256(), default_backend())

    # Self-sign the CSR to generate a certificate
    certificate = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        csr.subject
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True
    ).sign(private_key, SHA256(), default_backend())

    return private_key, certificate

def write_to_file(filename, data_list):
    with open(filename, "wb") as file:
        for data in data_list:
            file.write(data)

def main(num_certificates):
    private_keys = []
    certificates = []

    for _ in range(num_certificates):
        print(_)
        private_key, certificate = generate_certificate()
        
        private_keys.append(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
        
        certificates.append(certificate.public_bytes(serialization.Encoding.PEM))

    # Write all private keys to one file
    write_to_file(f"private_keys_{num_certificates}.pem", private_keys)

    # Write all certificates to another file
    write_to_file(f"certificates_{num_certificates}.pem", certificates)

if __name__ == "__main__":
    main(1000)  # Change 5 to the desired number of certificates
