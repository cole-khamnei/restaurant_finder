import subprocess

from typing import Optional

########################################################################################################################
### functions ###
########################################################################################################################

def subprocess_call(command: str):
    """"""
    return subprocess.Popen(command.split(), stdout=subprocess.PIPE).communicate()


class NordVPN:
    def __init__(self):
        self.status = self.check_status()
        self.group = "unknown"
        self.nord_vpn_command = 'C:\\Program Files\\NordVPN\\NordVPN.exe {args}'
        self.indent = " " * 3

    def check_status(self):
        """"""
        stdout, stderr = subprocess.Popen("netsh interface show interface".split(),
                                          stdout=subprocess.PIPE).communicate()
        vpn_connection_on_value = 'Enabled        Connected      Dedicated        NordLynx'
        for connection in stdout.decode("utf-8").strip().replace("\r", "").split("\n"):
             if vpn_connection_on_value == connection:
                    return True
        return False
    
    def connect(self, group: Optional[str] = None):
        """"""
        if self.check_status() and group == group:
            print("NordVPN already active.")
        else:
            init_command = self.nord_vpn_command.format(args='-c')
            if group:
                init_command += f' -g "{group}"'

            subprocess_call(init_command)

        time.sleep(1)
        assert self.check_status(), "Failed to connect to vpn."
        self.group = group

    def disconnect(self):
        """"""
        if self.check_status:
            subprocess_call(self.nord_vpn_command.format(args='-d'))
        
        assert not self.check_status(), "Failed to disconnect to vpn."
    
    def __repr__(self):
        s = "NordVPN\n"
        s += f"{self.indent}Status: {'Connected.' if self.check_status() else 'Disconnected'}\n"
        if self.group:
            s += f"{self.indent}Group: {self.group}"
        return s


########################################################################################################################
### End ###
########################################################################################################################