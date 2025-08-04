import sys
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
from io import BytesIO
from endesive.pdf import cms


def sign_pdf(pdf):
    date = datetime.datetime.utcnow()
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")
    dct = {
        "aligned": 8192,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": 0,
        # "sigbutton": True,
        # "sigfield": "Signature1",
        # "auto_sigfield": True,
        # "sigandcertify": True,
        "signaturebox": (470, 840, 570, 640),
        "signature": "People operations",
        "signature_img": "signature/signature.png",
        "contact": "apuertolara@provectus.com",
        "location": "Bogota",
        "signingdate": date,
        "reason": "Work Letter",
        "password": "123456",
    }
    with open("certs/certificate_2.p12", "rb") as fp:
        p12 = pkcs12.load_key_and_certificates(
            fp.read(), b"123456", backends.default_backend()
        )
    
    datas = cms.sign(pdf, dct, p12[0], p12[1], p12[2], "sha256")
    
    

    output_buffer = BytesIO()
    output_buffer.write(pdf)
    output_buffer.write(datas)
    signed_pdf = output_buffer.getvalue()

    return signed_pdf
