# SSH Config Language

Provides highlighting and snippets for [`~/.ssh/config`][man-ssh-config] and [`/etc/ssh/sshd_config`][man-sshd-config] files.


## Installation

This package [is available][pkg] via [Package Control][pkg-ctrl]. You can install it by searching for SSH in the "Install Package" interface or by cloning this repository in your Sublime Text "Packages" directory.


## Features

### Commands

- Open SSH Config File
- Open SSHD Config File

If these commands open the wrong file for you, open the Command Palette
(<kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> or
 <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>), search for
 "SSH Config: Settings", and put in content like this:

``` jsonc
{
    "file_locations": {
        "ssh_config": "~/.ssh/config",
        "sshd_config": "/etc/ssh/sshd_config",
        "known_hosts": "~/.ssh/known_hosts",
        "authorized_keys": "~/.ssh/authorized_keys",
    },
}
```


### SSH Config files

- `host`: create a new Host entry
- `match`: create a new Match entry
- Keyword completion for many \*Nix and \*BSD options
- Symbol Index for hosts and aliases
    (<kbd>Ctrl</kbd>+<kbd>R</kbd> or
     <kbd>Cmd</kbd>+<kbd>R</kbd>)
- Automatic indentation

Note that `~/.ssh/config` is not linked to the SSH Config syntax highlighting
out of the box. This is because the filename is shared by other formats (e.g.
`.git/config`) and we don't want to set the wrong highlighting for those. Solutions are [available on the wiki][wiki-activation].


### SSHD Config files

- Keyword completion for many \*Nix and \*BSD options
- Symbol Index for active and commented-out config options
    (<kbd>Ctrl</kbd>+<kbd>R</kbd> or
     <kbd>Cmd</kbd>+<kbd>R</kbd>)
- Automatic indentation


### Extras

- `authorized_keys` and `known_hosts` also have
    + Syntax highlighting
    + Symbol index
    + "Open file" commands
- PEM, PKCS1, PKCS8, and SSH keys have
    + Syntax
    + Symbol index for cert bundles
- Completion and highlighting for crypto stuff
    + Key types
    + KEX algorithms
    + Encryption ciphers
    + MACs


## Building

- Snippets, completions, and crypto names are built from the *src* directory in a simple Python script. Its only requirement is `pyyaml`.
- Changes to any of the above should be modified in YAML and rebuilt.
- Crypto items are sorted alphabetically, but any stems with longer versions are sorted to the bottom.
- Changes to syntaxes do not need rebuilding, but do need regression testing.


## Syntax testing

- Install this repository under Sublime Text `Packages` and name it `SSH Config`.
    + You can clone it there directly, move it, or symlink it.
- Open the project from under `Packages/SSH Config`.
- Open a syntax test file located in the *Tests* directory.
- Run the `Build With: Syntax Tests` command.
    + This is supplied by the `Default` Sublime Package, which is shipped with Sublime Text.
    + It is available on the Command Palette when a test file is open.

The [PackageDev][] package is helpful for writing tests but not required.


[man-ssh-config]: https://man7.org/linux/man-pages/man5/ssh_config.5.html
[man-sshd-config]: https://man7.org/linux/man-pages/man5/sshd_config.5.html
[pkg]: https://packagecontrol.io/packages/SSH%20Config
[pkg-ctrl]: https://packagecontrol.io
[wiki-activation]: https://github.com/robballou/sublimetext-sshconfig/wiki/Activate-SSH-Config-highlighting
[packagedev]: https://packagecontrol.io/packages/PackageDev
