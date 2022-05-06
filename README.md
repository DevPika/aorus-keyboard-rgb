# Aorus Keyboard RGB control
Reverse engineering USB messages using Wireshark to control RGB on Gigabyte Aorus 15P KD laptop

Tested on Aorus 15P KD-72US223SH laptop, Windows 10, Python v3.10

## Dependencies
* Python 3
* [pyusb](https://github.com/pyusb/pyusb) with libusb backend
  * If you face problems with libusb installation, this answer might help https://stackoverflow.com/questions/33972145/pyusb-on-windows-8-1-no-backend-available-how-to-install-libusb
* pyaudio for the audio sync script, use [this answer](https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14) if you face problems installing it on Windows

## Note for the audio sync script
If you would like the script to react to music playing on your machine, use a loopback device to direct output to an input device. A [pyaudio fork](https://github.com/intxcc/pyaudio_portaudio) which supports Windows sound loopback is mentioned in [this answer](https://stackoverflow.com/a/37218364). You can use [Stereo Mix](https://superuser.com/questions/753061/what-is-stereo-mix-supposed-to-be-used-for-in-windows) (which failed to work reliably for me) or use third-party software like [Voicemeeter](https://vb-audio.com/Voicemeeter/index.htm) on Windows.

## Current features:
* Set color and brightness for the static full keyboard mode
* Set different modes like Wave, Ripple, Raindrop, Fade on press etc.

## Future todo
* Per key customized lighting
* Integrate with [OpenRGB](https://gitlab.com/CalcProgrammer1/OpenRGB)
* ~Integrate with system audio using pyaudio similar to [this](https://github.com/CosmicSubspace/MSI-Keyboard-Lights) repo~ Done!
