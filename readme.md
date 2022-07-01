# Webcam Rock Paper Scissors 

A simple application that allows you to play Rock Paper Scissors with your Webcam.

Both multiplayer and singleplayer options are available

## Installation


First make sure that python3 and pip are installed

then 
Clone the project

```bash
  git clone https://gitlab-fnwi.uva.nl/webtech-in21/multimedia_iot.git
```

Go to the project directory

```bash
  cd multimedia_iot
```

Then make sure all dependecies are installed 

if on linux use 

```bash
  bash depen_installer.sh
```
You can now use

```bash
  python3 client/main.py
```

:)
## Run Locally

If you want to run your own server first make sure you did the regular install

Then run server setup on desired host machine

server can run both on localhost or public server

use.
```bash
  python3 server_install.py
```

copy the ip_adress obtained from the server Installation and port

then run

```bash
  python3 client_install.py
```
you are now ready

now run on all playing machines

```bash
  python3 client/main.py
```

and 
```bash
  python3 server/lobby_server.py
```
on the hosting machine
## Authors

- [Wessel van Sommeren](wessel.van.sommeren@gmail.com)
- [Alessio Silvério](alessio.silverio@student.uva.nl)
- [Thijs van Solt](thijs.van.solt@student.uva.nl)
- [Fedja](fedja.matti@student.uva.nl)
- [Bob kreugel](bobkreugel@student.uva.nl)
