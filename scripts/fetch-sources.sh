#!/usr/bin/env bash
# Fetch the 18 cutefishos repositories at their default-branch HEAD (or at the
# commits pinned in sources.lock) and repack them as deterministic tarballs for
# the cutefish source RPM.
#
# Usage: scripts/fetch-sources.sh [OUTPUT_DIR]
#
# Environment:
#   CUTEFISH_VERSION   version to stamp into the tarball names (default 0.1.0)
#   CUTEFISH_PINNED=1  use ./sources.lock instead of resolving upstream HEAD
set -Eeuo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
out=${1:-$here/build/sources}
version=${CUTEFISH_VERSION:-0.1.0}
lock=$here/sources.lock
org=cutefishos

# package name -> upstream repository
repos=(
    cutefish-toolkit=cutefish-toolkit
    cutefish-framework=cutefish-framework
    cutefish-qt-plugins=qt-plugins
    cutefish-icons=icons
    cutefish-core=cutefish-core
    cutefish-dm=cutefish-dm
    cutefish-filemanager=filemanager
    cutefish-terminal=terminal
    xdg-desktop-portal-cutefish=xdg-desktop-portal-cutefish
    cutefish-settings=settings
    cutefish-system-monitor=system-monitor
    cutefish-text-editor=text-editor
    cutefish-video-player=video-player
    cutefish-calendar=calendar
    cutefish-calculator=calculator
    cutefish-preview=preview
    cutefish-compositor=cutefish-compositor
    cutefish-wallpapers=wallpapers
)

declare -A pinned=()
if [[ ${CUTEFISH_PINNED:-0} == 1 && -f $lock ]]; then
    while read -r pkg _repo sha; do
        if [[ -n ${pkg:-} && ${pkg:0:1} != '#' ]]; then
            pinned[$pkg]=$sha
        fi
    done < "$lock"
    echo "using pins from $lock"
fi

mkdir -p "$out"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

tmp_lock=$work/sources.lock
: > "$tmp_lock"

for entry in "${repos[@]}"; do
    pkg=${entry%%=*}
    repo=${entry#*=}

    if [[ -n ${pinned[$pkg]:-} ]]; then
        sha=${pinned[$pkg]}
    else
        sha=$(git ls-remote "https://github.com/$org/$repo.git" HEAD | cut -f1)
    fi
    [[ ${sha:-} =~ ^[0-9a-f]{40}$ ]] || {
        echo "could not resolve $org/$repo HEAD" >&2
        exit 1
    }

    echo "==> $pkg <- $org/$repo@${sha:0:12}"
    curl -fsSL --retry 3 --retry-delay 2 \
        -o "$work/$repo.tar.gz" \
        "https://github.com/$org/$repo/archive/$sha.tar.gz"

    mkdir -p "$work/$pkg"
    tar -xzf "$work/$repo.tar.gz" -C "$work/$pkg" --strip-components=1
    rm -f "$work/$repo.tar.gz"

    # A predictable top-level directory, so the spec never has to know the
    # commit hash.
    mv "$work/$pkg" "$work/$pkg-$version"
    tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner \
        -czf "$out/$pkg-$version.tar.gz" -C "$work" "$pkg-$version"
    rm -rf "$work/$pkg-$version"

    printf '%s %s %s\n' "$pkg" "$repo" "$sha" >> "$tmp_lock"
done

sort -o "$tmp_lock" "$tmp_lock"
cp "$tmp_lock" "$out/sources.lock"
echo "wrote $(ls "$out"/*.tar.gz | wc -l) tarballs and $out/sources.lock"
