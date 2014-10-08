This is a first test at implementing device-side HomeKit in Python.

Currently it only supports the TLV-in-HTTP part of the pairing process.
Since the crypto stuff still doesn't work (and salt currently is just a dummy [0,0,0,...]) pairing can't succeed.

Pairing is basically SRP in TLV in HTTP.

I didn't (yet) implement the zeroconf/avahi announcement directly in the code, but using the following command does work:
```
avahi-publish -s Test _hap._tcp 50000 'md=Test' 's#=1' 'pv=1.0' 'ff=0' 'c#=2' 'id=1e:33:16:68:32:cd' 'sf=1'
```

From what I see you do not really need an MFi certified device to get HomeKit working, but you will receive a warning when adding the device to your home (so basically only once).

I'm not an expert, and I figured most of this stuff out by watching the traffic from iOS Simulator to HomeKit Acc Simulator and some disassembly of the HAPAccessoryKit framework, so it might not even work in the end.

Also I'm not sure if I'm going to continue development on this, because I decided to use MQTT for my smarthome-bullshit and do not really need this anymore.

