# cutefish-copr

Builds the [Cutefish](https://github.com/cutefishos) desktop environment as
Fedora RPMs and submits a fresh snapshot to a Copr project every day at
00:00 UTC.

One source package (`cutefish.spec`) contains all 18 upstream repositories and
produces one subpackage per component. `scripts/fetch-sources.sh` resolves the
default-branch HEAD of each repository, so a nightly run packages whatever
upstream shipped that day.

## Packages produced

`cutefish-toolkit`, `cutefish-framework`, `cutefish-qt-plugins`,
`cutefish-icons`, `cutefish-core`, `cutefish-dm`, `cutefish-filemanager`,
`cutefish-terminal`, `xdg-desktop-portal-cutefish`, `cutefish-settings`,
`cutefish-system-monitor`, `cutefish-text-editor`, `cutefish-video-player`,
`cutefish-calendar`, `cutefish-calculator`, `cutefish-preview`,
`cutefish-compositor`, `cutefish-wallpapers`, `cutefish-l10n`, plus the
`cutefish-desktop` meta package.

## One-time setup

### 1. Fedora account and Copr API token

1. Register at <https://accounts.fedoraproject.org/> and verify the email.
2. Sign in at <https://copr.fedorainfracloud.org/>.
3. Open <https://copr.fedorainfracloud.org/api/> and copy the config block it
   shows. Put it in `~/.config/copr`:

   ```ini
   [copr-cli]
   username = <your-fas-username>
   login = <a long hex string>
   token = <another long hex string>
   copr_url = https://copr.fedorainfracloud.org
   ```

   `chmod 600 ~/.config/copr`.

### 2. Create the Copr project

```bash
sudo dnf install -y copr-cli
./scripts/create-copr-project.sh
```

This creates a project with the `fedora-45-x86_64` chroot and enables network
access during builds (needed: the toolkit fetches Skia and the framework
fetches PDFium from their upstream repositories). The workflow passes
`--timeout 21600` (6 hours) to each build and submits it with `--nowait`, so
the GitHub job finishes once Copr has accepted the source package. Use
`COPR_CHROOTS="fedora-45-x86_64 fedora-45-aarch64"` to add chroots, or
`COPR_PROJECT=other-name` for a different project name.

### 3. GitHub repository and secret

The nightly job lives in `.github/workflows/nightly.yml`; `.github/workflows/ci.yml`
rebuilds the source package on every push and pull request and needs no
secrets. From this directory:

```bash
git add -A
git commit -m "Add nightly Cutefish Copr packaging"
gh auth login                       # the previous token has expired
gh repo create cutefish-copr --public --source=. --push
```

Use `--private` instead of `--public` if you prefer; scheduled workflows run
either way, but private repositories spend Actions minutes.

Then add the API token as a secret, and optionally the project name as a
variable:

```bash
gh secret set COPR_CONFIG < ~/.config/copr
gh variable set COPR_PROJECT --body cutefish
```

The secret is the whole `~/.config/copr` file; the workflow writes it to
`~/.config/copr` inside the Fedora container before calling `copr-cli`.

### 4. First build

Run the workflow once by hand:

```bash
gh workflow run nightly
gh run watch
```

Check the result at `https://copr.fedorainfracloud.org/coprs/<you>/cutefish/builds/`.
The first build compiles Skia and PDFium plus the whole stack, so expect
around one to two hours. Later nightly builds start from scratch too — Copr
does not cache the build root — but the sources are small.

### 5. Install

```bash
sudo dnf copr enable <you>/cutefish
sudo dnf install cutefish-desktop
```

Then pick the Cutefish session at the login screen, or switch the display
manager to `cutefish-dm` when you are happy with the session:

```bash
sudo systemctl disable gdm
sudo systemctl enable cutefish-dm
```

## How a nightly run works

1. `scripts/fetch-sources.sh` resolves `HEAD` for each repository, downloads
   `https://github.com/cutefishos/<repo>/archive/<sha>.tar.gz`, and repacks it
   as `<package>-0.1.0.tar.gz` with a fixed top-level directory and normalized
   ownership and mtimes.
2. `scripts/make-nightly-srpm.sh` stamps the date and run number into the spec
   (`Release: 1.<YYYYMMDD>.<run>`), adds the patches and the Fedora PAM files,
   and runs `rpmbuild -bs`.
3. The workflow uploads the SRPM to Copr. Copr builds each configured chroot
   from that SRPM; its build root has network access so the Skia and PDFium
   fetch scripts can run.

All builds of a given day share one source package, so the components are
always a consistent set.

## Pinning to known-good commits

By default every run takes upstream HEAD. If upstream breaks the build, commit
a `sources.lock` (the format is `<package> <repo> <sha>`, as written to
`build/sources/sources.lock`; the nightly run also prints it to the workflow
log under `Show source manifest`) and set `CUTEFISH_PINNED=1` in the workflow's
`Build nightly SRPM` step:

```yaml
      - name: Build nightly SRPM
        env:
          CUTEFISH_PINNED: 1
        run: ./scripts/make-nightly-srpm.sh
```

## Building locally

```bash
sudo dnf install -y rpm-build copr-cli copr-rpmbuild
./scripts/make-nightly-srpm.sh          # SRPM in build/out
copr-cli build cutefish build/out/*.src.rpm
```

To compile the stack on this machine without Copr, `dnf builddep` the SRPM and
run `rpmbuild --rebuild build/out/cutefish-*.src.rpm`. This needs about 8 GiB
of RAM for the Skia step with parallel jobs; pass `--define '_smp_build_ncpus 4'`
on a smaller machine.

## Patches and Fedora-specific files

- `patches/0001-cutefish-core-session-target.patch` — installs
  `cutefish-session.target` and starts it (and Fedora's `oo7` secret service)
  from the session launcher.
- `patches/0002-cutefish-qt-plugins-qt6.11.patch` — Qt 6.11 removed the
  per-window theme-change call; this is needed to build against Fedora 45's Qt.
- `sources/copr-sources/cutefish-dm*.pam` — Fedora PAM stacks replacing
  upstream's Debian `common-*` includes.
- `sources/copr-sources/cutefish-dm.tmpfiles.conf` — `/run/cutefish-dm` and
  `/var/lib/cutefish-dm` with the same permissions as GDM's directories.

SELinux contexts for the display manager are applied in the `%post` scriptlet
of `cutefish-dm`, mirroring what a manual Fedora install has to do.

## Notes

- `debug_package` is disabled: Skia and PDFium are linked statically and their
  debuginfo would be several gigabytes per nightly run.
- `%build` installs every component into a staging tree
  (`cutefish-0.1.0-stage`) so that the next component can link against it; rpm
  empties `%{buildroot}` right before `%install`, which then copies the staging
  tree over.
- The compositor package is built with the Fedora PAM stack explicitly
  (`-DCUTEFISH_PAM_CONFIG=...`) instead of relying on the build root having
  `/etc/pam.d/system-auth`.
- GitHub's cron scheduler can start a run a few minutes after 00:00 UTC; the
  timestamp in `Release` still uses the UTC date.
- Scheduled workflows only run from the default branch, and GitHub disables
  them in a repository with no pushes for 60 days. Any push re-enables them.
- If the workflow does not show up in the Actions tab (`gh workflow list` is
  empty even though Actions is enabled), GitHub did not register that blob:
  edit the file and push, the new blob is parsed again. This happened once
  with a workflow that arrived in the same push that created the repository.
