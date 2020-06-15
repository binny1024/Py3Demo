- Decimal 转换后的数据，赋值给字典，然后将字典转为 json 报错

需要显示转换
```python
# 下面需要显示转换
import json
from decimal import Decimal
dec = float(Decimal(12131.3132).quantize(Decimal('0.00000')))

data = {}
data['dec'] = dec

print('result', json.dumps(data))
```