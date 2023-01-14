#!/usr/bin/python
import math
import os

class UpowerHandler:
    __ac_icon = "ﮣ"
    __battery_icons = [ "", "", "", "", "" ]
    __bolt_icon = ""
    __separator = " "

    __signal_id = 3
    __file_path = "/tmp/block_results/dbus_upower_result"

    __system_bus = None
    __device_interface = None

    __watched_devices = []

    # kotelezo interface

    def __init__(self, system_bus, session_bus):
        self.__system_bus = system_bus
        upower = system_bus.get("org.freedesktop.UPower", "/org/freedesktop/UPower")

        properties = upower["org.freedesktop.DBus.Properties"]
        properties.PropertiesChanged.connect(self.main_properties_changed)

        self.__device_interface = upower["org.freedesktop.UPower"]
        self.__device_interface.DeviceAdded.connect(self.devices_changed)
        self.__device_interface.DeviceRemoved.connect(self.devices_changed)

    def handle(self):
        self.devices_changed("")    

    def get_name(self):
        return "U-Power D-Bus"

    def get_signal_id(self):
        return self.__signal_id

    def get_file_path(self):
        return self.__file_path

    # idaig

    def devices_changed(self, path):
        for device_tuple in self.__watched_devices:
            device_tuple[1].disconnect()
        
        self.__watched_devices.clear()

        power_device_paths = self.__device_interface.EnumerateDevices()

        for path in power_device_paths:
            device = self.__system_bus.get("org.freedesktop.UPower", path)
            
            properties = device["org.freedesktop.DBus.Properties"]

            subscription = properties.PropertiesChanged.connect(self.device_properties_changed)
            device_interface = device["org.freedesktop.UPower.Device"]

            self.__watched_devices.append((device_interface, subscription))

        self.something_changed()

    def main_properties_changed(self, interface_name, changed_properties, invalidated_properties):
        if "OnBattery" in changed_properties or "OnBattery" in invalidated_properties:
            self.something_changed()

    def device_properties_changed(self, interface_name, changed_properties, invalidated_properties):
        if "Percentage" in changed_properties or "Percentage" in invalidated_properties or "State" in changed_properties or "State" in invalidated_properties:
            self.something_changed()

    def format_percentage(self, percentage, charging):
        icon_index = 4
        if percentage <= 10:
            icon_index = 0
        elif percentage <= 30:
            icon_index = 1
        elif percentage <= 60:
            icon_index = 2
        elif percentage <= 80:
            icon_index = 3

        selected_icon = self.__battery_icons[icon_index]

        bolt_icon = ""
        if charging:
            bolt_icon = "{0} ".format(self.__bolt_icon)

        return "{0}{1}  {2:.0f}%".format(bolt_icon, selected_icon, percentage)

    def something_changed(self):
        on_battery = self.__device_interface.OnBattery

        outputs = []
        on_battery = True

        for device_tuple in self.__watched_devices:
            device = device_tuple[0]

            if not (device.Type == 2 and device.PowerSupply):
                continue

            outputs.append(self.format_percentage(device.Percentage, device.State == 1))
            on_battery = on_battery and not (device.State == 5)
       
        if on_battery:
            self.write_output(self.__separator.join(outputs))
        else:
            self.write_output("{0} AC".format(self.__ac_icon))
            return
    
    def write_output(self, output):
        with open(self.__file_path, "w") as f:
            f.write(output)

        os.system("pkill -RTMIN+{0} dwmblocks".format(self.__signal_id))
