import socket
import machine
import network
import ubinascii

ssid="Deez"
password="Winton123"

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_mac = wlan_sta.config('mac')
mac=ubinascii.hexlify(wlan_mac).decode().upper()

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
do_connect()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("192.168.43.29",42069))#May have to check the server code to get the ip
s.send("ESP")
s.send(mac.encode())
response=s.recv(1024).decode()
if response=="Disconnected":
    reason=s.recv(1024)
    s.close()
    print(f"Server rejected request because{reason}")
    exit()
elif response=="Connected":
    print("Connected to server")
else:
    print("Unknown")
    s.close()
    exit()
    
esp_led=machine.Pin(2, machine.Pin.OUT)
while True:
    command=s.recv(1024).decode()
    print(command)
    if command=="light_on":
        esp_led.on()
        print("LED Turned ON")
    elif command=="light_off":
        esp_led.off()
        print("LED Turned OFF")