#!/bin/bash
# 1.1 Create CA private key
openssl genrsa -out ca.key 2048

# 1.2 Create CA self-signed certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.crt \
  -subj "/C=CO/ST=State/L=City/O=MyOrganization/CN=MyRootCA"

# 2.1 Create private key for the signer
openssl genrsa -out signer.key 2048

# 2.2 Create a Certificate Signing Request (CSR)
openssl req -new -key signer.key -out signer.csr \
  -subj "/C=CO/ST=Bogota/L=Bogota/O=Provectus/CN=John Doe/emailAddress=email@email.com"

# 3.1 Create a config file for extensions (optional but recommended)
cat > signer.ext <<EOF
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
EOF

# 3.2 Sign the certificate with CA
openssl x509 -req \
  -in signer.csr \
  -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out signer.crt \
  -days 365 -sha256 \
  -extfile signer.ext
openssl pkcs12 -export \
  -out certificate_2.p12 \
  -inkey signer.key \
  -in signer.crt \
  -certfile ca.crt \
  -name "My PDF Signer" \
  -passout pass:123456

