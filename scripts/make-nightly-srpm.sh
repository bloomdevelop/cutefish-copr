#!/usr/bin/env bash
# Build the nightly source RPM in build/out/.
#
# Usage: scripts/make-nightly-srpm.sh
#
# Environment:
#   NIGHTLY_DATE  date stamp, default current UTC date (YYYYMMDD)
#   NIGHTLY_RUN   build counter, default current UTC epoch (keeps same-day
#                 rebuilds distinct in the repository)
set -Eeuo pipefail

here=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
version=$(sed -n 's/^%global version //p' "$here/cutefish.spec")
date=${NIGHTLY_DATE:-$(date -u +%Y%m%d)}
run=${NIGHTLY_RUN:-$(date -u +%s)}

sources=$here/build/sources
out=$here/build/out
rm -rf "$sources" "$out"
mkdir -p "$sources" "$out"

CUTEFISH_VERSION=$version "$here/scripts/fetch-sources.sh" "$sources"

install -m 644 "$here"/patches/*.patch "$sources/"
install -m 644 "$here"/sources/copr-sources/* "$sources/"

spec=$here/build/cutefish.spec
sed \
    -e "s/^%global nightly_date .*/%global nightly_date $date/" \
    -e "s/^%global nightly_run .*/%global nightly_run $run/" \
    "$here/cutefish.spec" > "$spec"

rpmbuild -bs \
    --define "_sourcedir $sources" \
    --define "_srcrpmdir $out" \
    --define "dist .fc45" \
    "$spec"

echo
ls -lh "$out"
