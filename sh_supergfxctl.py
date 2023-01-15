#!/usr/bin/python
import dmenu
from pydbus import SessionBus, SystemBus

mode_mappings = {
    "Hybrid": 0,
    "Integrated": 1,
    "VFIO": 2,
    "eGPU": 3,
    "None": 4
}

confirmation_mapping = {
    "Yes": True,
    "No": False
}

action_names = [ 
    "You need to log out for the mode switch to take place.", 
    "You need to switch to integrated graphics first.", 
    "You need to disable MUX before switching to this mode.", 
    "Successfully switched modes." 
]

def main():
    system_bus = SystemBus()
    session_bus = SessionBus()

    notifications = session_bus.get("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
    notification_service = notifications["org.freedesktop.Notifications"]

    dbus_path = system_bus.get("org.supergfxctl.Daemon", "/org/supergfxctl/Gfx")
    supergfxd_daemon = dbus_path["org.supergfxctl.Daemon"]

    supported_mode_indices = supergfxd_daemon.Supported()
    supported_modes = {k:v for k, v in mode_mappings.items() if v in supported_mode_indices}

    selected_mode = dmenu.show(supported_modes.keys(), prompt="Choose a new mode:")

    if selected_mode == None:
        print("Cancelled selection")
        return

    confirmation = dmenu.show(confirmation_mapping.keys(), prompt="Do you really want to switch to {0}?".format(selected_mode))

    if not (confirmation == None) and confirmation_mapping[confirmation]:
        selected_mode_index = mode_mappings[selected_mode]
        print("Switching to: {0} ({1})".format(selected_mode, selected_mode_index))

        action_required = action_names[supergfxd_daemon.SetMode(selected_mode_index)]

        notification_service.Notify(
            "sh_supergfxctl", # app_name
            0, # replaces_id
            "", # app_icon
            "GPU Mode Switch", # summary
            action_required, # body
            [], # actions
            {}, # hints
            -1 # expire_timeout
        )
    else:
        print("Rejected confirmation")

if __name__ == "__main__":
    main()
