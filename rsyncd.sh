# Used only for development.
# rsync the git from PC to device.

# TODO: Daemonize? 

REMOTE="192.168.1.12"
REMOTE_DIR="~/"
user="Termux"

rsync -av -e "ssh -p8022" \
    --no-owner --no-g --chmod u=rwX,g-rwx,o-rwx \
    --exclude-from './excludes.txt' \
    "$(pwd -P)" "${user}@${REMOTE}:${REMOTE_DIR}" 