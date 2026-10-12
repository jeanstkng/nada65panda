# Nada 65 Panda wireless recovery

Bluetooth and 2.4 GHz worked before this custom firmware was flashed. This
repository has neither a radio report transport nor handlers for its wireless
keycodes. The public KevinCain fork has the same omission. A related QMK MIIIW
driver uses UART, but its pinout and commands are not verified for this PCB.

Cerakey's [download page](https://www.cerakey.com/pages/download-x) currently
links the Nada manual and VIA JSON, but no Nada factory firmware image. A VIA
JSON describes key mappings; it cannot restore missing wireless firmware.

The [official manual](https://drive.google.com/file/d/1LBx_EZkt5oe-HYoHEI7DhaDuZo_5RdPB/view)
documents the factory wireless controls, not a firmware recovery procedure.
Those shortcuts cannot work in this custom build without their handlers.

Send this request through [Cerakey support](https://www.cerakey.com/pages/contact):

> My Nada 65 Panda worked over Bluetooth and 2.4 GHz before I flashed custom
> QMK firmware for cerakey/nada65panda. USB typing still works, but both wireless
> modes stopped working. Please provide the factory tri-mode firmware for my
> PCB revision and the recovery/flashing instructions. The keyboard definition
> uses USB VID 0x1480 and PID 0x6351 (HyphaRF KB351). If available, please also
> provide the wireless-enabled QMK source or the radio controller's pinout and
> communication protocol. Please confirm whether the radio module needs a
> separate update and whether restoring firmware preserves receiver pairing.

Once a matching image is available, verify its PCB revision and flash address
before flashing. Firmware for another HyphaRF or MIIIW keyboard is not a verified
replacement. If firmware/source cannot be obtained, implementing wireless needs
the PCB's controller markings, wiring, and protocol measurements.

The `firmware/*_powerfix.bin` files only address lighting power handling. They
do not restore wireless and have not yet been tested on hardware. To flash the
VIA build using the bootloader procedure already documented in README.md:

```sh
qmk flash firmware/cerakey_nada65panda_via_powerfix.bin
```

After flashing, test unplugging USB in wired mode, reconnecting, host sleep and
wake, and a side-light mode that was already set to off. Its saved mode and
brightness should survive these operations.
