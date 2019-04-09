# SSH Config Language

Provides highlighting and snippets for [`~/.ssh/config`][man-ssh-config] and [`/etc/ssh/sshd_config`][man-sshd-config] files.

## Installation

This package [is available][pkg] via [Package Control][pkg-ctrl]. You can install it by searching for SSH in the "Install Package" interface or by cloning this repository in your Sublime Text "Packages" directory.

## Snippets and Completions

To see autocomplete, hit <kbd>Ctrl</kbd>+<kbd>Space</kbd> for an on-demand list or add this entry to syntax-specific settings to see the list while typing:

``` json
{
    "auto_complete_selector": "text.ssh_config, text.sshd_config"
}
```

### SSH Config

- `host`: create a new Host entry
- `match`: create a new Match entry
- Keyword completion for Linux and BSD options

### SSHD Config

- Keyword completion for Linux and BSD options

## Commands

- **Open SSH Config File**
- **Open SSHD Config File**

## To-Do

- Configurable file locations for the "open" commands
- Better SSHD Config syntax

[man-ssh-config]: http://man7.org/linux/man-pages/man5/ssh_config.5.html
[man-sshd-config]: http://man7.org/linux/man-pages/man5/sshd_config.5.html
[pkg]: https://packagecontrol.io/packages/SSH%20Config
[pkg-ctrl]: https://packagecontrol.io
