#!/usr/bin/python

class SupergfxdHandler:
    __signal_id = 4
    __file_path = "/tmp/block_results/dbus_supergfxd_result"

    __supergfxd_daemon = None

    __current_mode_index = 0
    _mode_names = ["Hybrid", "Integrated", "VFIO", "eGPU", "None"]

    __current_power_index = 0
    __power_names = ["Active", "Suspended", "Off", "Disabled", "MUX", "Unknown"]
    __power_icons = ["", "鈴", "ﮤ", "", "", ""]

    # kotelezo interface

    def __init__(self, system_bus, session_bus):
        dbus_path = system_bus.get("org.supergfxctl.Daemon", "/org/supergfxctl/Gfx")
        self.__supergfxd_daemon = dbus_path["org.supergfxctl.Daemon"]

    def handle(self):
        self.__supergfxd_daemon.NotifyAction.connect(self.event_handler)
        self.__supergfxd_daemon.NotifyGfx.connect(self.event_handler)
        self.__supergfxd_daemon.NotifyGfxStatus.connect(self.event_handler)

        self.something_changed()

    def get_name(self):
        return "Supergfxd D-Bus"

    def get_signal_id(self):
        return self.__signal_id

    def get_file_path(self):
        return self.__file_path

    # idaig

    def event_handler(self, value):
        self.something_changed()

    def something_changed(self):
        self.__current_mode_index = self.__supergfxd_daemon.Mode()
        self.__current_power_index = self.__supergfxd_daemon.Power()

        output = "{0}  {1}".format(self.__power_icons[self.__current_power_index], self._mode_names[self.__current_mode_index])

        self.write_output(output)
