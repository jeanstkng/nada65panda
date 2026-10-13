# [Nada 65 Panda](https://www.cerakey.com/products/nada-65-panda-keyboard)

This is the first ceramic keycap mechanical keyboard -- 'Smoothest and Thockiest Typing'

- Keyboard Maintainer: [zquestz](https://github.com/zquestz)
- Hardware Supported: Nada 65 Panda

Open [shortcuts.html](shortcuts.html) in your browser for an offline reference to lighting controls and all Windows/Mac key mappings.

This custom firmware currently supports USB typing only. `DEV_BT1`, `DEV_BT2`,
`DEV_BT3`, `DEV_RF24`, and `DEV_CLR` are mapped but have no implementation;
Bluetooth and 2.4 GHz require the manufacturer's firmware or a verified driver
for this PCB. The binaries already in `firmware/` are custom QMK builds, not
factory recovery images. See [wireless recovery](docs/wireless-recovery.md).

The `*_powerfix.bin` builds turn the separate side-light controller off when
USB is inactive or suspended and restore its selected mode when USB resumes.
They also enable QMK's normal RGB suspend handling. These builds have passed
compilation and mocked controller tests, but still need testing on the keyboard.
Run the controller test with `python3 tests/test_side_lights.py` (requires `cc`).

You will need a working QMK installation to build the new firmware.

Note, if the keyboard appears USB "dead" keyboard (error -71 in dmesg), you might try the following first to get the keyboard back into a responsive state:
- Put the physical connection switch in the center position (wired mode)
- Reconnect USB. This custom keymap has no FN + Spacebar wired/reset command.


See the [build environment setup](https://docs.qmk.fm/#/getting_started_build_tools) and the [make instructions](https://docs.qmk.fm/#/getting_started_make_guide) for more information. Brand new to QMK? Start with our [Complete Newbs Guide](https://docs.qmk.fm/#/newbs).

Once you are all setup.

1. Copy the `nada65panda` folder to the keyboards directory in your QMK installation.

```
mkdir -p ~/src/qmk_firmware/keyboards/cerakey
cp -r nada65panda ~/src/qmk_firmware/keyboards/cerakey/
```

If updating an existing copy, remove `keyboards/cerakey/nada65panda/info.json`
from your QMK installation. `keyboard.json` replaces it; current QMK rejects
having both files in the same keyboard directory.

2. Build the new firmware, with Via support.

```
qmk compile -kb cerakey/nada65panda -km via
```

3. Start flashing the firmware.

```
qmk flash cerakey_nada65panda_via.bin
```

4. When prompted for bootloader mode, hold Fn and press B (Windows or Mac). Saved VIA mappings can override the firmware defaults. Holding Esc during a fresh startup is the Bootmagic fallback and clears saved EEPROM settings.

5. Wait till the flashing process is complete.

6. Disconnect your keyboard and reconnect it!

7. Profit!
