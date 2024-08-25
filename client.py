import socket

HOST = 'localhost'
PORT = 50505

def send_command(command, key=None, value=None, value_type=None):
  """Sends a command to the server.

  Args:
    command: The command to send.
    key: The key for the command, if applicable.
    value: The value for the command, if applicable.
    value_type: The type of the value, if applicable.

  Returns:
    The server's response to the command.
  """

  message = '{};{};{};{}'.format(command, key or '', value or '', value_type or '')
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(message.encode('utf-8'))
    response = sock.recv(4096).decode('utf-8')
  return response

def main():
   while 1:
    message = input('Введите комманду: ')
    if(message == 'EXIT'):
      break
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(message.encode('utf-8'))
        response = sock.recv(4096).decode('utf-8')
        print(response)
    

if __name__ == '__main__':
  main()