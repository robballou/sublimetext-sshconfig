import sublime
import sublime_plugin
from os.path import expandvars


def get_file_location(identifier):
    settings = sublime.load_settings('SSH Config.sublime-settings')
    user_setting = settings.get('file_locations')
    if user_setting:
        if identifier in user_setting:
            return expandvars(user_setting[identifier])
        else:
            print('Could not find {} key in "file_locations"'
                  ''.format(identifier))
    return expandvars(settings.get(
        'default_file_locations')[sublime.platform()][identifier])


def open_new_view(instance, identifier):
    window = instance.view.window()
    if not window:
        print('Missing window for view')
        return
    view = window.open_file(get_file_location(identifier))
    return view


class OpenSshConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = open_new_view(self, 'ssh_config')
        if not view:
            return

        if sublime.load_settings('SSH Config.sublime-settings').get(
                'force_ssh_config_syntax'):
            syntax = 'Packages/SSH Config/syntax/SSH Config.sublime-syntax'
            view.settings().set('syntax', syntax)


class OpenSshdConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = open_new_view(self, 'sshd_config')


class OpenKnownHostsFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = open_new_view(self, 'known_hosts')


class OpenAuthorizedKeysFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = open_new_view(self, 'authorized_keys')
