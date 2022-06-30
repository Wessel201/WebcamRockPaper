import socket, requests
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   


print("Your Computer IP Address is:"+IPAddr) 


print("Do you want to install server on localhost? (y/n)")
local = input("Choice: ")

if local == "y":
    host = "localhost"
    port = 5000
    print(f"IP adress is: {IPAddr}")
else:
    r = requests.request("GET","http://ipinfo.io/ip")
    host = r.text
    print("Make sure entered port + 20 are open for tcp connections")
    port = input("PORT:")
    print(f"IP adress is: {host}")

with open("server/server_config.txt", "w+") as f:
    f.write(f"{host}\n{port}")
    print("Server config file created")
    print("Add ip adress to client config file")