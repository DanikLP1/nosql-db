import socket
import time

HOST = 'localhost'
PORT = 50505
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
STATS = {
    'PUT': {
        'success': 0,
        'error': 0
    },
    'GET': {
        'success': 0,
        'error': 0
    },
    'GETLIST': {
        'success': 0,
        'error': 0
    },
    'PUTLIST': {
        'success': 0,
        'error': 0
    },
    'INCREMENT': {
        'success': 0,
        'error': 0
    },
    'APPEND': {
        'success': 0,
        'error': 0
    },
    'DELETE': {
        'success': 0,
        'error': 0
    },
    'STATS': {
        'success': 0,
        'error': 0
    },
}

DATA = {}

def parse_message(data):
    try:
        command, key, value, value_type = map(str.strip, data.strip().split(';'))
    except:
        return 'Invalid input! Expected: COMMAND; [KEY]; [VALUE]; [VALUE_TYPE]'
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
    else:
        value = None
    return command, key, value

def update_stats(command, success):
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1

def handle_put(key, value):
    DATA[key] = value
    return (True, 'key [{}] set to [{}]'.format(key, value))

def handle_get(key):
    if key not in DATA:
        return (False, 'Error: key [{}] not found'.format(key))
    else:
        return (True, DATA[key])

def handle_putlist(key, value):
    return handle_put(key, value)

def handle_getlist(key):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value, list):
        return (False, 'ERROR: key [{}] contains non-list value ([{}])'.format(key, value))
    else:
        return return_value
    
def handle_increment(key):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value, list):
        return (False, 'ERROR: key [{}] contains non-list value ([{}])'.format(key, value))
    else:
        DATA[key] = value + 1
        return (True, 'key [{}] incremented'.format(key, value))

def handle_append(key, value):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value, list):
        return (False, 'ERROR: key [{}] contains non-list value ([{}])'.format(key, value))
    else:
        DATA[key].append(value)
        return (True, 'key [{}] had value [{}] appendend'.format(key, value))
    
def handle_delete(key):
    if key not in DATA:
        return(False, 'ERROR: key[{}] not found and could not be deleted'.format(key))
    else:
        del DATA[key]
    
def handle_stats():
    return (True, str(STATS))

COMMAND_HANDER = {
    'PUT': handle_put,
    'GET': handle_get,
    'GETLIST': handle_getlist,
    'PUTLIST': handle_putlist,
    'INCREMENT': handle_increment,
    'APPEND': handle_append,
    'DELETE': handle_delete,
    'STATS': handle_stats
}
    
def main():
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)
    print('Listening on {}'.format((HOST, PORT)))
    while 1:
        connection, address = SOCKET.accept()
        print('{} New connection from {}'.format(
            time.strftime(('%Y/%m/%d %H:%M:%S INFO'), time.localtime()),
            address))
        data = connection.recv(4096).decode()
        print(data)
        command, key, value = parse_message(data)
        if command == 'STATS':
            response = handle_stats()
        elif command in ('GET', 'GETLIST', 'INCREMENT', 'DELETE'):
            response = COMMAND_HANDER[command](key)
        elif command in ('PUT', 'PUTLIST', 'APPEND'):
            response = COMMAND_HANDER[command](key, value)
        else:
            response = (False, 'Unknown command type: {}'.format(command))
        update_stats(command, response[0])
        data = '{};\n{}\n'.format(response[0], response[1])
        connection.sendall(bytearray(data, 'utf-8'))
        connection.close()
    
if __name__ == '__main__':
    main()
