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
