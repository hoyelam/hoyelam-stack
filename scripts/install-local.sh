#!/bin/sh
set -eu

hoyelam_stack_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
hoyelam_stack_codex_root=${HOYELAM_STACK_CODEX_SKILLS_ROOT:-${CODEX_HOME:-${HOME}/.codex}/skills}

link_path() {
    hoyelam_stack_source=$1
    hoyelam_stack_target=$2
    hoyelam_stack_parent=$(dirname -- "$hoyelam_stack_target")
    mkdir -p "$hoyelam_stack_parent"
    if [ -L "$hoyelam_stack_target" ] && [ "$(readlink "$hoyelam_stack_target")" = "$hoyelam_stack_source" ]; then
        printf 'Already linked: %s\n' "$hoyelam_stack_target"
        return
    fi
    if [ -e "$hoyelam_stack_target" ] || [ -L "$hoyelam_stack_target" ]; then
        printf 'Conflict: %s already exists\n' "$hoyelam_stack_target" >&2
        exit 1
    fi
    ln -s "$hoyelam_stack_source" "$hoyelam_stack_target"
    printf 'Linked: %s -> %s\n' "$hoyelam_stack_target" "$hoyelam_stack_source"
}

install_codex() {
    for hoyelam_stack_skill_dir in "$hoyelam_stack_root"/skills/*; do
        hoyelam_stack_skill_name=$(basename -- "$hoyelam_stack_skill_dir")
        link_path "$hoyelam_stack_skill_dir" "$hoyelam_stack_codex_root/$hoyelam_stack_skill_name"
    done
}

case ${1:-codex} in
    codex)
        install_codex
        ;;
    *)
        printf 'Usage: %s [codex]\n' "$0" >&2
        exit 2
        ;;
esac
