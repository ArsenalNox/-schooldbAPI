"""
    Обрабатывает заданиие для модуля по химии,
    заменяя все индексы html элементом для 
    корректного отображения в веб браузере 
"""

import re

search_string = """
А) MgO и Al2O3
Б) H3PO4 и Na3PO4
В) NaBr и BaBr2
A1
1) H2SO4
А) Cu0 → Cu+2
Б) Cl+5 → Cl-1
В) N-3 → N+2
H2O3
"""

result_string = re.sub(
        r'(?<=[a-zA-Z]){1,2}[1-9]', 
        r'<sub>\g<0></sub>', 
        search_string)
result_string = re.sub(
        r'(?<=[a-zA-Z]){1,2}((0)|(\+|\-)[0-9])', 
        r'<sup>\g<0></sup>', 
        result_string)

print(result_string)
