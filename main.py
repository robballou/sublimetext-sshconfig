import sublime
import sublime_plugin


class OpenSshConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = '~/.ssh/config'
        self.view.window().open_file(filename)


class OpenSshdConfigFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = '/etc/ssh/sshd_config'
        self.view.window().open_file(filename)


class OpenKnownHostsFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = '~/.ssh/known_hosts'
        self.view.window().open_file(filename)


class OpenAuthorizedKeysFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = '~/.ssh/authorized_keys'
        self.view.window().open_file(filename)
