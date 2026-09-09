#!/usr/bin/env bash
# Install the figure toolchain on macOS or Debian/Ubuntu (including WSL).
set -euo pipefail

figure_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
with_fiziko=true
dry_run=false
check_only=false

usage() {
  printf '%s\n' \
    'Usage: bash fig-generator/install.sh [--no-fiziko] [--dry-run | --check]' \
    '' \
    'Default: install missing dependencies and the pinned fiziko library.' \
    '  --no-fiziko  Set up only plots and schematics.' \
    '  --dry-run    Print planned installations without making changes.' \
    '  --check      Check the installation without downloads or changes.' \
    '  --help       Show this help.' \
    '' \
    'macOS requires Homebrew; Debian/Ubuntu uses apt-get and sudo when needed.' \
    'Run as your normal user. Package installers may request administrator access.'
}

die() { printf 'install: %s\n' "$*" >&2; exit 1; }
say() { printf '%s\n' "$*"; }
have() { command -v "$1" >/dev/null 2>&1; }
run() {
  printf '+'
  printf ' %q' "$@"
  printf '\n'
  if ! "$dry_run"; then "$@"; fi
}

for argument in "$@"; do
  case "$argument" in
    --no-fiziko) with_fiziko=false ;;
    --dry-run) dry_run=true ;;
    --check) check_only=true ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; die "Unknown option: $argument" ;;
  esac
done
if "$dry_run" && "$check_only"; then die '--dry-run and --check cannot be combined'; fi

platform="$(uname -s)"
case "$platform" in
  Darwin)
    # MacTeX's installer updates future shells; make its tools available now too.
    if [ -d /Library/TeX/texbin ]; then export PATH="/Library/TeX/texbin:$PATH"; fi
    if ! have brew; then
      for brew_bin in /opt/homebrew/bin /usr/local/bin; do
        if [ -x "$brew_bin/brew" ]; then export PATH="$brew_bin:$PATH"; break; fi
      done
    fi
    ;;
  Linux) ;;
  *) die "Unsupported platform: $platform. Use macOS, Debian/Ubuntu, or Ubuntu under WSL." ;;
esac

python_ready() {
  have python3 && python3 -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1
}

tex_ready() {
  have lualatex && have kpsewhich || return 1
  local package
  for package in standalone.cls fontspec.sty unicode-math.sty tikz.sty pgfplots.sty \
      texgyrepagella-regular.otf texgyrepagella-math.otf; do
    kpsewhich "$package" >/dev/null 2>&1 || return 1
  done
  if "$with_fiziko"; then
    kpsewhich luamplib.sty >/dev/null 2>&1 || return 1
  fi
}

missing_python=false
missing_tex=false
missing_poppler=false
missing_rsvg=false
python_ready || missing_python=true
tex_ready || missing_tex=true
if ! have pdftocairo || ! have pdfinfo; then missing_poppler=true; fi
have rsvg-convert || missing_rsvg=true

if "$check_only"; then
  python_ready || die 'Python 3.10+ is required; run the installer without --check.'
elif "$missing_python" || "$missing_tex" || "$missing_poppler" || "$missing_rsvg"; then
  case "$platform" in
    Darwin)
      have brew || die 'Install Homebrew from https://brew.sh, then rerun this script.'
      # Never replace an existing TeX distribution or conflict with a BasicTeX cask.
      if "$missing_tex" && { have lualatex || have kpsewhich; }; then
        die 'The existing TeX installation is incomplete. Install the packages reported by figure.py doctor (and luamplib for engravings), then rerun. See USAGE.md.'
      fi
      packages=()
      if "$missing_python"; then packages+=(python); fi
      if "$missing_poppler"; then packages+=(poppler); fi
      if "$missing_rsvg"; then packages+=(librsvg); fi
      if [ "${#packages[@]}" -gt 0 ]; then run brew install "${packages[@]}"; fi
      if "$missing_tex"; then run brew install --cask mactex-no-gui; fi
      if ! "$dry_run"; then
        export PATH="$(brew --prefix)/bin:/Library/TeX/texbin:$PATH"
        hash -r
      fi
      ;;
    Linux)
      have apt-get || die 'Automatic Linux installation requires apt-get. See USAGE.md for the required tools.'
      apt_command=(apt-get)
      if [ "$(id -u)" -ne 0 ]; then
        if have sudo; then apt_command=(sudo apt-get)
        elif ! "$dry_run"; then die 'sudo is required to install system packages as a non-root user'
        else apt_command=(sudo apt-get)
        fi
      fi
      packages=(ca-certificates)
      if "$missing_python"; then packages+=(python3); fi
      if "$missing_tex"; then
        packages+=(texlive-luatex texlive-latex-extra texlive-pictures
                   texlive-fonts-recommended tex-gyre fonts-texgyre-math)
        if "$with_fiziko"; then packages+=(texlive-metapost); fi
      fi
      if "$missing_poppler"; then packages+=(poppler-utils); fi
      if "$missing_rsvg"; then packages+=(librsvg2-bin); fi
      run "${apt_command[@]}" update
      run "${apt_command[@]}" install -y --no-install-recommends "${packages[@]}"
      ;;
  esac
fi

if "$dry_run"; then
  if "$with_fiziko"; then
    say 'If the pinned fiziko cache is missing or changed:'
    run python3 "$figure_dir/figure.py" install-fiziko
  fi
  say 'The installer will finish by checking tool and package availability.'
  exit 0
fi

python_ready || die 'Python 3.10+ is required. Use a current Python on PATH (Ubuntu 22.04+ / Debian 12+ provide one).'
if "$with_fiziko" && ! "$check_only"; then
  if python3 -c 'import sys; sys.path.insert(0, sys.argv[1]); import figure; figure.fiziko_path()' "$figure_dir" >/dev/null 2>&1; then
    say 'Pinned fiziko is already installed and verified.'
  else
    run python3 "$figure_dir/figure.py" install-fiziko
  fi
fi

if ! report="$(python3 "$figure_dir/figure.py" doctor)"; then
  printf '%s\n' "$report"
  die 'The toolchain is incomplete; inspect the missing entries above and USAGE.md.'
fi
printf '%s\n' "$report"
if "$with_fiziko"; then
  python3 -c 'import json, sys; sys.exit(not json.loads(sys.argv[1])["engraved_ready"])' "$report" \
    || die 'Engraved figures need luamplib and pinned fiziko. Run the installer without --check, or use --no-fiziko.'
fi
say 'Figure toolchain ready. See USAGE.md for repeatable render tests.'
if [ "$platform" = Darwin ]; then
  say 'If a new terminal cannot find lualatex, add /Library/TeX/texbin to PATH.'
fi
