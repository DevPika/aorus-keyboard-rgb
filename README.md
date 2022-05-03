# Aorus Keyboard RGB control
Reverse engineering USB messages using Wireshark to control RGB on Gigabyte Aorus 15P KD laptop

Tested on Aorus 15P KD-72US223SH laptop, Windows 10, Python v3.10

## Dependencies
* Python 3
* [pyusb](https://github.com/pyusb/pyusb) with libusb backend
  * If you face problems with libusb installation, this answer might help https://stackoverflow.com/questions/33972145/pyusb-on-windows-8-1-no-backend-available-how-to-install-libusb

## Current features:
* Set color and brightness for the static full keyboard mode
* Set different modes like Wave, Ripple, Raindrop, Fade on press etc.

## Future todo
* Per key customized lighting
* Integrate with [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB)
* Integrate with system audio using pyaudio similar to [this](https://github.com/CosmicSubspace/MSI-Keyboard-Lights) repo
