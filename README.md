# pair-sonos
A simple python script that stereo pairs Sonos speakers. Nothing more, nothing less.

The script uses [SoCo](https://github.com/SoCo/SoCo) to discover and find UID:s of Sonos devices.

Tested on Python 3.6.5.

## Prerequisites

Make sure SoCo and Requests are installed. Use pip to install them:

```
pip install soco requests
```

Depending on your Python installation, you might have to change `pip` to `pip3`.

## Usage

List devices:
```
python pair.py list
```

If that doesn't work, the problem might be that SoCo needs to know the IP of your network interface. Try:
```
python pair.py list my_ip_goes_here
```

Pair speakers:
```
python pair.py pair ip_of_master ip_of_slave
```

The **master** will act as the **left** speaker.

Unpair speakers:
```
python pair.py unpair ip_of_master
```

Depending on your Python installation, you might have to change `python` to `python3`.
