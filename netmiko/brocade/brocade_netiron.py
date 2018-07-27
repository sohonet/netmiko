from __future__ import unicode_literals
import re
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko.ssh_exception import NetMikoTimeoutException


class BrocadeNetironBase(CiscoSSHConnection):
    def save_config(self, cmd='write memory', confirm=False):
        """Save Config"""
        return super(BrocadeNetironBase, self).save_config(cmd=cmd, confirm=confirm)

    def enable(self, cmd='enable', pattern='(user name|password):', re_flags=re.IGNORECASE):
        output = ""
        msg = "Failed to enter enable mode. Please ensure you pass " \
              "the 'secret' argument to ConnectHandler."
        if not self.check_enable_mode():
            self.write_channel(self.normalize_cmd(cmd))
            try:
                output += self.read_until_prompt_or_pattern(pattern=pattern, re_flags=re_flags)
                if 'User Name' in output:
                    self.write_channel(self.normalize_cmd(self.username))
                    self.write_channel(self.normalize_cmd(self.secret))
                else:
                    self.write_channel(self.normalize_cmd(self.secret))
                output += self.read_until_prompt()
            except NetMikoTimeoutException:
                raise ValueError(msg)
            if not self.check_enable_mode():
                raise ValueError(msg)
        return output


class BrocadeNetironSSH(BrocadeNetironBase):
    pass


class BrocadeNetironTelnet(BrocadeNetironBase):
    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get('default_enter')
        kwargs['default_enter'] = '\r\n' if default_enter is None else default_enter
        super(BrocadeNetironTelnet, self).__init__(*args, **kwargs)
