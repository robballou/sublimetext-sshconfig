# SSH Config Language

Provides highlighting and snippets for `~/.ssh/config` and `/etc/ssh/sshd_config` files.

## Installation

This package is available via [Package Control](http://wbond.net/sublime_packages/package_control). You can install it by searching for SSH in the "Install Package" interface or by cloning this package in your Sublime Text "Packages" directory.

## Snippets and Completions

To see autocomplete, hit <kbd>Ctrl</kbd>+<kbd>Space</kbd> for an on-demand list or add this entry to syntax-specific settings to see the list while typing:

``` json
{
    "auto_complete_selector": "text.ssh_config, text.sshd_config"
}
```

### SSH Config

- host: create a new `Host` entry
- match: create a new `Match` entry
- Many completion words

### SSHD Config

- Many completion words

## Commands

- Open SSH Config
- Open SSHD Config
