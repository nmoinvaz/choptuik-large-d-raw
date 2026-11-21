# sourced by run1064.sh (#1064 on dh610)
WT=/home/nathan/Source/choptuik-large-d-1060
VENV=/home/nathan/Source/venv-i1058
RAW=/home/nathan/Source/choptuik-large-d-raw
SD=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
OUT=${OUT1064:-$SD}   # OUT1064 only for the dry test of the cap and the control-failed branch
S=I966-dh370/ks_chain3b/leg13_D260.8483_ks293/anm_pin3_D261.0721.npz
S_BLOB=bd2c69a4d3fd16dffbc7ce340f50946772ca0b80
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
stamp() { date -u '+%F %T'; }
