import sys
from cryptography import x509
from typing import List, cast

from cryptography.hazmat.backends import default_backend

f_p = sys.argv[1]
fp_cont = open(f_p, 'r')
cert_content = fp_cont.read()

def extract_dns_subject_alternative_names(certificate: x509.Certificate) -> List[str]:
    """Retrieve all the DNS entries of the Subject Alternative Name extension.
    """
    subj_alt_names: List[str] = []
    try:
        san_ext = certificate.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
        san_ext_value = cast(x509.SubjectAlternativeName, san_ext.value)
        subj_alt_names = san_ext_value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        pass
    except x509.DuplicateExtension:
        # Fix for https://github.com/nabla-c0d3/sslyze/issues/420
        # Not sure how browsers behave in this case but having a duplicate extension makes the certificate invalid
        # so we just return no SANs (likely to make hostname validation fail, which is fine)
        pass

    return subj_alt_names

content = bytes(cert_content, encoding="utf-8")
certificate = x509.load_pem_x509_certificate(content, default_backend())
print(extract_dns_subject_alternative_names(certificate))