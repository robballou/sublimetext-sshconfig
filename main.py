from __future__ import annotations
from sublime import load_settings, platform
from sublime_plugin import TextCommand
from os.path import expandvars


def get_file_location(identifier: str) -> str:
    settings = load_settings('SSH Config.sublime-settings')
    user_setting: dict[str, str] | None = settings.get('file_locations')
    if user_setting:
        if identifier in user_setting:
            return expandvars(user_setting[identifier])
        else:
            print('Could not find {} key in "file_locations"'.format(identifier))
    default_settings: dict[str, dict[str, str]] = settings.get('default_file_locations')
    setting: dict[str, str] = default_settings[platform()]
    return expandvars(setting[identifier])


def open_new_view(instance: TextCommand, identifier: str):
    window = instance.view.window()
    if not window:
        print('Missing window for view')
        return
    view = window.open_file(get_file_location(identifier))
    return view


class OpenSshConfigFileCommand(TextCommand):
    def run(self, edit, **kwargs) -> None:
        view = open_new_view(self, 'ssh_config')
        if not view:
            return

        if load_settings('SSH Config.sublime-settings').get(
                'force_ssh_config_syntax'):
            syntax = 'Packages/SSH Config/syntax/SSH Config.sublime-syntax'
            view.settings().set('syntax', syntax)


class OpenSshdConfigFileCommand(TextCommand):
    def run(self, edit, **kwargs) -> None:
        view = open_new_view(self, 'sshd_config')


class OpenKnownHostsFileCommand(TextCommand):
    def run(self, edit, **kwargs) -> None:
        view = open_new_view(self, 'known_hosts')


class OpenAuthorizedKeysFileCommand(TextCommand):
    def run(self, edit, **kwargs) -> None:
        view = open_new_view(self, 'authorized_keys')
