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


class OpenSshConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view.window().open_file(get_file_location('ssh_config'))

        if sublime.load_settings('SSH Config.sublime-settings').get(
                'force_ssh_config_syntax'):
            syntax = 'Packages/SSH Config/SSH Config.sublime-syntax'
            view.settings().set('syntax', syntax)


class OpenSshdConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('sshd_config'))


class OpenKnownHostsFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('known_hosts'))


class OpenAuthorizedKeysFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('authorized_keys'))
