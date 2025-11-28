with import <nixpkgs> {};

mkShell {
  buildInputs = [
    python3
    python3Packages.ipython
    python3Packages.pip
    neovim
    curl
  ];
  shellHook = ''
    # Optionally: upgrade pip and install pyflyby in the local environment
    pip install --user pyflyby
    pip install --user labml-nn

    # Download custom nvim config
    export NVIM_CONFIG_DIR="$HOME/.config/nvim-nix-shell"
    mkdir -p "$NVIM_CONFIG_DIR"

    # Download the config if it doesn't exist or is older than 1 day
    if [ ! -f "$NVIM_CONFIG_DIR/init.lua" ] || [ $(find "$NVIM_CONFIG_DIR/init.lua" -mtime +1 2>/dev/null | wc -l) -gt 0 ]; then
      echo "Downloading custom nvim config..."
      curl -fsSL https://raw.githubusercontent.com/rlogger/nvim-config/refs/heads/main/init.lua \
        -o "$NVIM_CONFIG_DIR/init.lua"
    fi

    # Create nvim alias to use custom config
    alias nvim='nvim -u "$NVIM_CONFIG_DIR/init.lua"'
    alias vim='nvim -u "$NVIM_CONFIG_DIR/init.lua"'

    echo "Custom nvim config loaded from: $NVIM_CONFIG_DIR/init.lua"
  '';
}
