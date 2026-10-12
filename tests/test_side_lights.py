"""Run with python3 tests/test_side_lights.py; requires a host C compiler."""
from pathlib import Path
import subprocess
import tempfile

source = (Path(__file__).resolve().parents[1] / "nada65panda.c").read_text()
callbacks = source[source.index("static bool side_lights_suspended"):
                   source.index("deferred_token loop10hz_token")]
harness = r"""
#include <assert.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#define I2C_STATUS_SUCCESS 0
uint8_t side_cmd[9] = {0x5a, 0x12, 1, 2, 3, 4, 5, 0, 0};
uint8_t sent[9];
int calls, status, sleeps, wakes;
bool connected;
int i2c_transmit(int address, const uint8_t *cmd, int size, int timeout) {
    assert(address == 0x8a && size == 9 && timeout == 100);
    memcpy(sent, cmd, 9);
    calls++;
    return status;
}
bool usb_connected_state(void) { return connected; }
void suspend_power_down_user(void) { sleeps++; }
void suspend_wakeup_init_user(void) { wakes++; }
"""
checks = r"""
int main(void) {
    uint8_t original[9];
    memcpy(original, side_cmd, 9);
    status = -1;
    suspend_power_down_kb();
    assert(!side_lights_suspended && calls == 1 && sleeps == 1);
    status = 0;
    suspend_power_down_kb();
    assert(side_lights_suspended && calls == 2 && sent[1] == 0);
    assert(memcmp(original, side_cmd, 9) == 0);
    for (int i = 0; i < 9; i++) {
        if (i != 1) assert(sent[i] == original[i]);
    }
    suspend_power_down_kb();
    assert(calls == 2);
    side_cmd[1] = 3; // Lighting shortcuts also stay dark while disconnected.
    transmit_side_lights(!usb_connected_state());
    assert(calls == 3 && sent[1] == 0 && side_cmd[1] == 3);
    side_cmd[1] = original[1];
    suspend_wakeup_init_kb();
    assert(calls == 3 && wakes == 1); // Still disconnected.
    connected = true;
    status = -1;
    suspend_wakeup_init_kb();
    assert(side_lights_suspended && calls == 4);
    status = 0;
    suspend_wakeup_init_kb();
    assert(!side_lights_suspended && memcmp(sent, original, 9) == 0);
    side_cmd[1] = 0; // The user chose to leave the lights off.
    suspend_power_down_kb();
    suspend_wakeup_init_kb();
    assert(sent[1] == 0 && side_cmd[1] == 0);
}
"""
with tempfile.TemporaryDirectory() as tmp:
    c_file = Path(tmp) / "side_lights.c"
    executable = Path(tmp) / "side_lights"
    c_file.write_text(harness + callbacks + checks)
    subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror",
                    str(c_file), "-o", str(executable)], check=True)
    subprocess.run([str(executable)], check=True)
print("Side-light suspend, restore, and I2C retry checks passed.")
