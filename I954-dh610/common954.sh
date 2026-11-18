# sourced by build954.sh, checksA.sh and checksB.sh (#954 on dh610)
SRC=/home/nathan/Source/choptuik-large-d
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I954-dh610
R=/home/nathan/scratch954/raw
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
PRED=I903-win2/ks_chain/leg07_D222.0000_ks240/pred_pin3_D229.5165.npz
T=8
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
stamp() { date -u '+%F %T'; }
