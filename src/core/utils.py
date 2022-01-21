import json

def find_json_values(id, json_repr):
    results = []

    def _decode_dict(a_dict):
        try: results.append(a_dict[id])
        except KeyError: pass
        return a_dict

    json.load(open('src/core/properties.json'))  # Return value ignored.
    return results

#json_repr = '{"P1": "ss", "Id": 1234, "P2": {"P1": "cccc"}, "P3": [{"P1": "aaa"}]}'
#print(find_json_values('P1', json_repr))

json_str = json.load(open('src/core/properties.json'))
print(json_str['version'])