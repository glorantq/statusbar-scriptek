#!/usr/bin/python
import os

class ConnmanHandler:
    __ethernet_icon = ""    
    __offline_icon = "睊"
    __separator = " "

    __signal_id = 2
    __file_path = "/tmp/block_results/dbus_connman_result"

    __connman = None
    __connman_manager = None

    # kotelezo interface

    def __init__(self, system_bus, session_bus):
        self.__connman = system_bus.get("net.connman", "/")
        self.__connman_manager = self.__connman["net.connman.Manager"]

    def handle(self):
        self.__connman_manager.ServicesChanged.connect(self.services_changed)
        self.services_changed([], [])

    def get_name(self):
        return "Connman D-Bus"

    def get_signal_id(self):
        return self.__signal_id

    def get_file_path(self):
        return self.__file_path

    # idaig

    def format_unknown(self, object):
        name = str(object["Name"] or "Unknown")

        return name

    def format_ethernet(self, object):
        name = str(object["Name"] or "Wired")
    
        ethernet_object = object["Ethernet"]
        interface = str(ethernet_object["Interface"] or "?")

        return "{0}  {1} [{2}]".format(self.__ethernet_icon, name, interface)

    def services_changed(self, changed, removed):
        formatted_services = []

        services = self.__connman_manager.GetServices()
        for service in services:
            key = service[0]
            properties = service[1]

            type = properties["Type"]
            state = properties["State"]

            if(state != "ready" and state != "online"):
                continue
        
            formatter = self.format_unknown
            # ide majd i guess be kell irni wifit meg
            # bluetootht ha lesz outputom megnezni
            # az milyen
            match type:
                case "ethernet":
                    formatter = self.format_ethernet

            formatted_services.append(formatter(properties))

        if len(formatted_services) == 0:
            formatted_services.append("{0}  Offline".format(self.__offline_icon))
    
        output = self.__separator.join(formatted_services)
        with open(self.__file_path, "w") as f:
            f.write(output)
	
        print(output)
        os.system("pkill -RTMIN+{0} dwmblocks".format(self.__signal_id))
   
