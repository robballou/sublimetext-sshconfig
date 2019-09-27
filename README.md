# SSH Config Language

Provides highlighting and snippets for [`~/.ssh/config`][man-ssh-config] and [`/etc/ssh/sshd_config`][man-sshd-config] files.

## Installation

This package [is available][pkg] via [Package Control][pkg-ctrl]. You can install it by searching for SSH in the "Install Package" interface or by cloning this repository in your Sublime Text "Packages" directory.

## Snippets and Completions

If you do not see on-demand autocomplete, check for an `auto_complete_selector` line in your Syntax-specific Settings file. If it says `text.ssh_config`, remove the whole line. If one does not exist, you can try adding

``` json
{
    "auto_complete_selector": "source.ssh_config, source.sshd_config"
}
```

### SSH Config

- `host`: create a new Host entry
- `match`: create a new Match entry
- Keyword completion for many Linux and BSD options
- Symbol Index for hosts and aliases (<kbd>Ctrl</kbd>+<kbd>R</kbd> or <kbd>Cmd</kbd>+<kbd>R</kbd>)

### SSHD Config

- Keyword completion for many Linux and BSD options
- Symbol Index for active config options (<kbd>Ctrl</kbd>+<kbd>R</kbd> or <kbd>Cmd</kbd>+<kbd>R</kbd>)

## Commands

- **Open SSH Config File**
- **Open SSHD Config File**

## Extras

- `authorized_keys` and `known_hosts` also have
    + Syntax highlighting
    + Symbol index
    + Available commands (though you have to map them yourself)

## To-Do

- Configurable file locations for the "open" commands
- (Even) better SSHD Config syntax

[man-ssh-config]: http://man7.org/linux/man-pages/man5/ssh_config.5.html
[man-sshd-config]: http://man7.org/linux/man-pages/man5/sshd_config.5.html
[pkg]: https://packagecontrol.io/packages/SSH%20Config
[pkg-ctrl]: https://packagecontrol.io
