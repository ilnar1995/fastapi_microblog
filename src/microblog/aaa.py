def remove_duplicates(lst):
    unique_sets = set(frozenset(inst.items()) for inst in lst)
    return [dict(s) for s in unique_sets]

dic = [{"key1": "value1"}, {"k1": "v1", "k2": "v2", "k3": "v3"}, {}, {}, {"key1": "value1"}, {"key1": "value1"}, {"key2": "value2"}]
dic1 = {1:'dsdf', "2,0":'sdsd', "2,0":'sdsd'}
print(dic1)

a = remove_duplicates(dic)
print(a)

