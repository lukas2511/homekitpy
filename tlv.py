import base64
import pprint
import sys

tlv_types = {
    'auth_method': 0x00,
    'user': 0x01,
    'salt': 0x02,
    'public_key': 0x03,
    'proof': 0x04,
    'encrypted_data': 0x05,
    'auth_tag': 0x06,
    'state': 0x07,
    'status': 0x08,
    'retry_delay': 0x09,
    'certificate': 0x0a,
    'mfiproof': 0x0b,
    'admin': 0x0c,
}

tlv_status = {
    'ok': 0x00,
    'unknown': 0x01,
    'auth': 0x02,
    'toomanyattempts': 0x03,
    'unknownpeer': 0x04,
    'maxpeers': 0x05,
    'maxtries': 0x06,
}

def get_tlv_name(type_id):
    return list(tlv_types)[tlv_types.values().index(type_id)]

def get_tlv_id(type_name):
    return tlv_types[type_name]

def pack(input):
    output = []
    for package in input:
        while package['length'] > 0:
            if package['length'] == 1 and not isinstance(package['data'], list):
                package['data'] = [package['data']]
            output += [chr(get_tlv_id(package['type']))]
            if package['length'] > 255:
                #print("Type: %s, Length: %s" % (hex(get_tlv_id(package['type']))[2:], "ff"))
                output += [chr(255)]
                package['length'] -= 255
            else:
                #print("Type: %s, Length: %s" % (hex(get_tlv_id(package['type']))[2:], hex(package['length'])[2:]))
                output += [chr(package['length'])]
                package['length'] = 0
            output += package['data'][0:255]
            package['data'] = package['data'][255:]
    output = bytearray(output)
#    for i in range(0, len(output)):
        #sys.stdout.write("%.2x" % int(output[i]))
        #sys.stdout.write(" ")
    return str(output)

def unpack(input):
    input = bytearray(input)
    mark = 0
    output = []
    while(mark < len(input)):
        p_type = get_tlv_name(input[mark])
        mark += 1
        p_len = input[mark]
        mark += 1
        p_data = list(input[mark:mark+p_len])
        mark += p_len
        if len(output) and p_type == output[-1]['type'] and output[-1]['length'] >= 255:
            output[-1]['length'] += p_len
            output[-1]['data'] += p_data
        else:
            package = {'type': p_type, 'length': p_len, 'data': p_data}
            output.append(package)

    return output

