import sublime
import sublime_plugin


def get_file_location(identifier):
    settings = sublime.load_settings('SSH Config.sublime-settings')
    user_setting = settings.get('file_locations')
    if user_setting:
        if identifier in user_setting:
            return user_setting[identifier]
        else:
            print('Could not find {} key in "file_locations"'
                  ''.format(identifier))
    return settings.get(
        'default_file_locations')[sublime.platform()][identifier]


class OpenSshConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('ssh_config'))


class OpenSshdConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('sshd_config'))


class OpenKnownHostsFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('known_hosts'))


class OpenAuthorizedKeysFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file(get_file_location('authorized_keys'))
