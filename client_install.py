print("Please enter ip adress of server")
ip = input("IP: ")

print("Please enter port of server")
port = input("PORT: ")

with open("client/client_config.txt", "w") as f:
    f.write(f"{ip}\n{port}")
    print("client config file created")