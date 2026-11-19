# sourced by the #997 scripts on dh610
WT=/home/nathan/Source/choptuik-large-d-997        # origin/main 459180e6, Python only
WTV=/home/nathan/Source/choptuik-large-d-967       # the venv with the kernel (d96a09a1)
RAW=/home/nathan/Source/choptuik-large-d-raw
OUT=$RAW/I997-dh610
R=/home/nathan/scratch997/raw
ST=I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M160.npz
NODES=0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9
export PATH=$HOME/.local/bin:$HOME/.cargo/bin:$PATH
stamp() { date -u '+%F %T'; }
