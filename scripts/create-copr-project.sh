#!/usr/bin/env bash
# Create (or update) the Copr project that receives the nightly builds.
# Needs ~/.config/copr from https://copr.fedorainfracloud.org/api/ .
#
# Usage: scripts/create-copr-project.sh [extra copr-cli options]
#
# Environment:
#   COPR_PROJECT  project name (default: cutefish)
#   COPR_CHROOTS  space-separated chroots (default: fedora-45-x86_64)
set -Eeuo pipefail

project=${COPR_PROJECT:-cutefish}
chroots=${COPR_CHROOTS:-fedora-45-x86_64}

args=()
for chroot in $chroots; do
    args+=(--chroot "$chroot")
done

info=(
    --description "Nightly snapshots of the Cutefish desktop environment, built from github.com/cutefishos"
    --instructions "Install with: sudo dnf copr enable \$USERNAME/$project && sudo dnf install cutefish-desktop"
    --enable-net on
)

if copr-cli get "$project" >/dev/null 2>&1; then
    echo "updating Copr project $project"
    copr-cli modify "$project" "${args[@]}" "${info[@]}" "$@"
else
    echo "creating Copr project $project"
    copr-cli create "$project" "${args[@]}" "${info[@]}" "$@"
fi

copr-cli get "$project"
