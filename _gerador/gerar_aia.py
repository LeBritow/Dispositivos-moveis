# -*- coding: utf-8 -*-
# Regenera o TorreEV.aia byte-a-byte a partir dos bytes embutidos em aia_bytes.py.
# Uso: python3 gerar_aia.py   -> grava ../TorreEV.aia
import base64, os, sys

try:
    import aia_bytes
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import aia_bytes

OUT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'TorreEV.aia'))
with open(OUT, 'wb') as f:
    import zipfile
    with zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, b64 in aia_bytes.ARQUIVOS.items():
            z.writestr(name, base64.b64decode(b64))
print('AIA regenerado:', OUT)
