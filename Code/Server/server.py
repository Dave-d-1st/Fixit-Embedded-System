import socket
import json
with open(r"C:\Users\davem\Documents\Code\fixit\Fixit-Embedded-System\Code\Server\mac.json","r") as f:
    mac_addresses=json.load(f)
user=[]
esps=[]
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip=socket.gethostbyname(socket.gethostname())
server.bind((ip,42069))
print(f"http://{ip}:42069")
server.listen()

def broadcast_esp(message):
    for esp in esps:
        esp.send(message.encode())
def webpage(temperature, state):
    #Template HTML
    html = f"""<!DOCTYPE html>
<html>
<body>
<form action="./lighton">
<input type="submit" value="Light on" />
</form>
<form action="./lightoff">
<input type="submit" value="Light off" />
</form>
<p>LED is {state}</p>
<p>Temperature is {temperature}</p>
</body>
</html>"""
    return str(html)
while True:
    client,address=server.accept()
    state="OFF"
    request=client.recv(1024).decode()
    print(request)
    if request.split()[0] == "GET":
        user.append(client)
        #Should make this a function
        client.send('HTTP/1.0 200 OK\n'.encode())
        client.send('Content-Type: text/html\nSet-Cookie: Deez=Nutz\n'.encode())
        client.send('\n'.encode())
        if request.split()[1]=='/lighton?':
            broadcast_esp("light_on")
            state = 'ON'
        elif request.split()[1] =='/lightoff?':
            broadcast_esp("light_off")
            state = 'OFF'
        html = webpage(0, state)
        client.send(html.encode())
        print(client,address)
        client.close()
    elif request=="ESP":
        mac=client.recv(1024).decode()
        if mac in mac_addresses:
            client.send("Connected".encode())
        else:
            client.send("Disconnected".encode())
            client.send("Unknown mac address")
            client.close()
        print(address)
        esps.append(client)