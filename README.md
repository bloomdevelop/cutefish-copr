# cutefish-copr

> [!NOTE]
> This is nightly build, which resolves the latest commit from `HEAD` (per repository), so there's a good chance
> it may break anything, if it's related to packaging, please file an issue in here (and not blame Cutefish developers!).
>
> Additionally, if it still broken I may set the `CUTEFISH_PINNED` to 1 until fixes are in place.

Builds the [Cutefish](https://github.com/cutefishos) desktop environment as
Fedora RPMs and submits a fresh snapshot to a Copr project every day at
00:00 UTC.

One source package (`cutefish.spec`) contains all 18 upstream repositories and
produces one subpackage per component. `scripts/fetch-sources.sh` resolves the
default-branch HEAD of each repository, so a nightly run packages whatever
upstream shipped that day.

## Available packages

- `cutefish-desktop` (meta-package)
- `cutefish-toolkit`
- `cutefish-framework`
- `cutefish-qt-plugins`
- `cutefish-icons`
- `cutefish-core`
- `cutefish-dm`
- `cutefish-filemanager`
- `cutefish-terminal`
- `xdg-desktop-portal-cutefish`
- `cutefish-settings`
- `cutefish-system-monitor`
- `cutefish-text-editor`
- `cutefish-video-player`
- `cutefish-calendar`
- `cutefish-calculator`
- `cutefish-preview`
- `cutefish-wallpapers`
- `cutefish-l10n`

### Unavailable package

| Package                 | Description                                                                                | Notes                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `cutefish-computer-use` | MCP server which lets LLM agents see and use the Cutefish desktop, only when user allow it | Will be built later today                                                                                                                                                                                                                                                                                                                                                                                                |
| `reef`                  | Part of cutefish that lets you run macOS application                                       | Not open sourced yet, check for [reason why](https://cutefish.org/blog/running-mac-apps/#is-it-open-source:~:text=Not%20for%20now.%20This%20is%20a%20large%20investment%20and%20a%20feature%20that%20sets%20Cutefish%20apart%2C%20and%20it%20needs%20to%20be%20protected%20while%20it%20grows.%20Opening%20it%20later%20is%20possible%2C%20for%20example%20once%20community%20sponsorship%20can%20sustain%20the%20work.) |

## Patches and Fedora-specific files

This COPR contains Fedora-specific files/patches in order to be usable without intetionally breaking it:

- `patches/0001-cutefish-core-session-target.patch`: installs
  `cutefish-session.target` and starts it (and Fedora's `oo7` secret service)
  from the session launcher.
- `patches/0002-cutefish-qt-plugins-qt6.11.patch`: Qt 6.11 removed the
  per-window theme-change call, this is needed to build against Fedora 45's Qt.
- `patches/0003-cutefish-qt-plugins-menu-bar.patch`: the platform theme
  exports each window's menu bar to the shell from a D-Bus connection of its
  own, so applications whose session bus stops delivering calls (Krita) still
  show their menus in the top bar.
- `patches/0004-cutefish-toolkit-fontconfig-freetype.patch`: includes
  `fontconfig/fcfreetype.h`, where fontconfig declares `FcFreeTypeQueryAll`;
  `fontconfig/fontconfig.h` does not include it.
- `sources/copr-sources/cutefish-dm*.pam`: Fedora PAM stacks replacing
  upstream's Debian `common-*` includes.
- `sources/copr-sources/cutefish-dm-auth-substack`: auth/password substack
  for `cutefish-dm`, mirroring `gdm-password-auth-substack`. `password-auth`'s
  `pam_unix` is `sufficient`, so with a plain `include` the stack ends at
  `pam_unix` and the `pam_oo7` lines after it never run, the login keyring
  then stays locked and GNOME Online Accounts finds no credentials after
  login. Inside a substack the `sufficient` only ends the substack and the
  `pam_oo7` lines are reached.
- `sources/copr-sources/cutefish-dm.tmpfiles.conf`, `/run/cutefish-dm` and
  `/var/lib/cutefish-dm`: with the same permissions as GDM's directories.

SELinux contexts for the display manager are applied in the `%post` scriptlet
of `cutefish-dm`, mirroring what a manual Fedora install has to do.
