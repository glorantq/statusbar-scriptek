#!/usr/bin/python

class AsusdHandler:
    __signal_id = 5
    __file_path = "/tmp/block_results/dbus_asusd_result"

    __asusd_profile_daemon = None

    __current_profile_index = 0
    __profile_names = ["Balanced", "Performance", "Quiet"]

    # kotelezo interface

    def __init__(self, system_bus, session_bus):
        dbus_path = system_bus.get("org.asuslinux.Daemon", "/org/asuslinux/Profile")
        self.__asusd_profile_daemon = dbus_path["org.asuslinux.Daemon"]

    def handle(self):
        self.__asusd_profile_daemon.NotifyProfile.connect(self.profile_changed)
        self.profile_changed(self.__asusd_profile_daemon.ActiveProfile())

    def get_name(self):
        return "Asusd D-Bus"

    def get_signal_id(self):
        return self.__signal_id

    def get_file_path(self):
        return self.__file_path

    # idaig

    def event_handler(self, value):
        self.something_changed()

    def profile_changed(self, profile):
        self.__current_profile_index = profile

        output = "  {0}".format(self.__profile_names[self.__current_profile_index])

        self.write_output(output)
