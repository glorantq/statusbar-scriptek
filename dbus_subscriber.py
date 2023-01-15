#!/usr/bin/python
import os

from pydbus import SessionBus, SystemBus
from gi.repository import GLib

from dbus_connman import ConnmanHandler
from dbus_upower import UpowerHandler
from dbus_supergfxd import SupergfxdHandler
from dbus_asusd import AsusdHandler

from functools import partial

session_bus = SessionBus()
system_bus = SystemBus()

def main():
    handlers = [ 
        ConnmanHandler(system_bus, session_bus),
        UpowerHandler(system_bus, session_bus),
        SupergfxdHandler(system_bus, session_bus),
        AsusdHandler(system_bus, session_bus)
    ]

    for handler in handlers:
        name = handler.get_name()
        signal = handler.get_signal_id()
        path = handler.get_file_path()

        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("Loading...")

        print("\"{0}\" -> {1} (signal {2})".format(name, path, signal))

        handler.write_output = partial(write_output, handler)

    for handler in handlers:
        handler.handle()

    loop = GLib.MainLoop()
    loop.run()

def write_output(object, content):
    with open(object.get_file_path(), "w") as f:
            f.write(content)
            
    os.system("pkill -RTMIN+{0} dwmblocks".format(object.get_signal_id()))

if __name__ == "__main__":
    main()