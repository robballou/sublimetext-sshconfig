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
- Keyword completion for many \*Nix and \*BSD options
- Symbol Index for hosts and aliases
    (<kbd>Ctrl</kbd>+<kbd>R</kbd> or
     <kbd>Cmd</kbd>+<kbd>R</kbd>)

### SSHD Config

- Keyword completion for many \*Nix and \*BSD options
- Symbol Index for active and commented-out config options
    (<kbd>Ctrl</kbd>+<kbd>R</kbd> or
     <kbd>Cmd</kbd>+<kbd>R</kbd>)

## Commands

- Open SSH Config File
- Open SSHD Config File

If these open the wrong file for you, make a `SSH Config.sublime-settings` file in your `Packages/User` folder, and put in content like this:

``` json
{
    "file_locations": {
        "ssh_config": "~/.ssh/config",
        "sshd_config": "/etc/ssh/sshd_config",
        "known_hosts": "~/.ssh/known_hosts",
        "authorized_keys": "~/.ssh/authorized_keys"
    }
}
```

## Extras

- `authorized_keys` and `known_hosts` also have
    + Syntax highlighting
    + Symbol index
    + (unmapped) "Open file" commands

## To-Do

- Completion and highlighting for crypto stuff (MACs, ciphers, algos)
- Better highlighting for paths

[man-ssh-config]: https://man7.org/linux/man-pages/man5/ssh_config.5.html
[man-sshd-config]: https://man7.org/linux/man-pages/man5/sshd_config.5.html
[pkg]: https://packagecontrol.io/packages/SSH%20Config
[pkg-ctrl]: https://packagecontrol.io
