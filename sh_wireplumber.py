#!/usr/bin/python
import subprocess
import os
import sys

_output_icons = [ "", "", "" ]
_output_icon_muted = "婢"

_input_icon = ""
_input_icon_muted = ""

_signal_id = 1

def get_status(device):
    volume_process = subprocess.run(["wpctl", "get-volume", device], stdout=subprocess.PIPE)
    volume_raw = volume_process.stdout.decode("utf-8").strip()

    volume = round(float(volume_raw.split("Volume:")[-1].split(" ")[1]) * 100)
    muted = "muted" in volume_raw.lower()

    return (volume, muted)

def format_output():
    output_status = get_status("@DEFAULT_AUDIO_SINK@")

    chosen_icon = _output_icons[-1]

    if output_status[0] <= 10:
        chosen_icon = _output_icons[0]
    elif output_status[0] <= 50:
        chosen_icon = _output_icons[1]

    if output_status[1]:
        chosen_icon = _output_icon_muted

    return "{0}  {1}%".format(chosen_icon, output_status[0])

def format_input():
    input_status = get_status("@DEFAULT_AUDIO_SOURCE@")

    chosen_icon = _input_icon
    if input_status[1]:
        chosen_icon = _input_icon_muted

    return "{0}  {1}%".format(chosen_icon, input_status[0])

def format_volume_status():
    print("{0} {1}".format(format_input(), format_output()))

def main():
    if len(sys.argv) == 1:
        format_volume_status()
        return

    if sys.argv[-1] == "inc":
        os.system("wpctl set-volume @DEFAULT_AUDIO_SINK@ 1%+")

    if sys.argv[-1] == "dec":
        os.system("wpctl set-volume @DEFAULT_AUDIO_SINK@ 1%-")

    if sys.argv[-1] == "mute":
        os.system("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")

    os.system("pkill -RTMIN+{0} dwmblocks".format(_signal_id))

if __name__ == "__main__":
    main()