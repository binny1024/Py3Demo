import decimal
import json
from decimal import Decimal
dec = decimal.Decimal(23) / decimal.Decimal("1.05")

print(dec)

dec = float(Decimal(12131.3132).quantize(Decimal('0.00000')))

data = {}
data['dec'] = dec

print('result', json.dumps(data))
