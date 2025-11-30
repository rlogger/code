with import <nixpkgs> {};

mkShell {
  buildInputs = [
    # Python and dependencies
    python3
    python3Packages.ipython
    python3Packages.pip
    python3Packages.black
    python3Packages.isort
    python3Packages.ruff

    # Neovim and core tools
    neovim
    curl
    git

    # Telescope dependencies
    ripgrep
    fd

    # Git UI
    lazygit

    # Language servers and formatters
    pyright
    lua-language-server
    stylua

    # Treesitter dependencies (C compiler)
    gcc
  ];

  shellHook = ''
    # Install Python packages
    pip install --user pyflyby
    pip install --user labml-nn

    # Setup custom nvim config directory
    export NVIM_CONFIG_DIR="$HOME/.config/nvim-nix-shell"
    export NVIM_DATA_DIR="$HOME/.local/share/nvim-nix-shell"
    mkdir -p "$NVIM_CONFIG_DIR"
    mkdir -p "$NVIM_DATA_DIR"

    # Download the init.lua config if it doesn't exist or is older than 1 day
    if [ ! -f "$NVIM_CONFIG_DIR/init.lua" ] || [ $(find "$NVIM_CONFIG_DIR/init.lua" -mtime +1 2>/dev/null | wc -l) -gt 0 ]; then
      echo "Downloading custom nvim config..."
      curl -fsSL https://raw.githubusercontent.com/rlogger/nvim-config/refs/heads/main/init.lua \
        -o "$NVIM_CONFIG_DIR/init.lua"
    fi

    # Set XDG directories for Neovim to use isolated plugin storage
    export XDG_CONFIG_HOME="$HOME/.config"
    export XDG_DATA_HOME="$HOME/.local/share"

    # Create nvim wrapper function to use custom config with isolated data directory
    nvim() {
      command nvim -u "$NVIM_CONFIG_DIR/init.lua" --cmd "set runtimepath^=$NVIM_DATA_DIR" "$@"
    }
    vim() {
      nvim "$@"
    }
    export -f nvim vim

    echo "Custom nvim config loaded from: $NVIM_CONFIG_DIR/init.lua"
    echo "Plugins will be installed to: $NVIM_DATA_DIR"
    echo ""
    echo "Available tools:"
    echo "  - Neovim with Lazy.nvim plugin manager"
    echo "  - LSP servers: pyright (Python), lua-language-server"
    echo "  - Formatters: black, isort, ruff, stylua"
    echo "  - Git tools: lazygit"
    echo "  - Search tools: ripgrep, fd"
  '';
}
