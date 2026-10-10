# Path to your oh-my-zsh configuration.
ZSH=$HOME/.oh-my-zsh

# Hide username in prompt
DEFAULT_USER=`whoami`

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
plugins=(git composer macos)

source $ZSH/oh-my-zsh.sh

# set numeric keys
# 0 . Enter
bindkey -s "^[0p" "0"
bindkey -s "^[0l" "."
bindkey -s "^[0M" "^M"
# 1 2 3
bindkey -s "^[Oq" "1"
bindkey -s "^[Or" "2"
bindkey -s "^[Os" "3"
# 4 5 6
bindkey -s "^[Ot" "4"
bindkey -s "^[Ou" "5"
bindkey -s "^[Ov" "6"
# 7 8 9
bindkey -s "^[Ow" "7"
bindkey -s "^[Ox" "8"
bindkey -s "^[Oy" "9"
# + -  * /
bindkey -s "^[Ok" "+"
bindkey -s "^[Om" "-"
bindkey -s "^[Oj" "*"
bindkey -s "^[Oo" "/"

# Load the shell dotfiles, and then some:
# * ~/.dotfiles-custom can be used for other settings you don’t want to commit.
for file in ~/.dotfiles/shell/.{exports,aliases,functions}; do
	[ -r "$file" ] && [ -f "$file" ] && source "$file"
done

for file in ~/.dotfiles-custom/shell/.{exports,aliases,functions,zshrc}; do
	[ -r "$file" ] && [ -f "$file" ] && source "$file"
done
unset file

. $HOME/.dotfiles/shell/z.sh

# Sudoless npm https://github.com/sindresorhus/guides/blob/master/npm-global-without-sudo.md
NPM_PACKAGES="${HOME}/.npm-packages"
export PATH="$PATH:$NPM_PACKAGES/bin"
# Preserve MANPATH if you already defined it somewhere in your config.
# Otherwise, fall back to `manpath` so we can inherit from `/etc/manpath`.
export MANPATH="${MANPATH-$(manpath)}:$NPM_PACKAGES/share/man"

# Import ssh keys in keychain
ssh-add --apple-load-keychain 2>/dev/null;

# Extra paths
export PATH=$PATH:/opt/homebrew/bin
export PATH="$HOME/.composer/vendor/bin:$PATH"
export PATH=/usr/local/bin:$PATH
export PATH=~/.config/phpmon/bin:$PATH

export PNPM_HOME="/Users/marc/Library/pnpm"
export PATH="$PNPM_HOME:$PATH"

eval "$(thefuck --alias)"
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"

export NODE_EXTRA_CA_CERTS="$HOME/.config/valet/CA/LaravelValetCASelfSigned.pem"

export CLAUDE_CODE_NO_FLICKER=1

source ~/agp-completions.sh

# zoxide must be initialized at the very end of this file
eval "$(zoxide init zsh --cmd cd)"
