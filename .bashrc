# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi


umask 022

# Uncomment the following line if you don't like systemctl's auto-paging feature:
# export SYSTEMD_PAGER=

# User specific aliases and functions


alias cp='cp -i'
alias mv='mv -i'
alias rm='rm -i'

alias ll='ls -alF -h -G'
alias la='ls -A'
alias f='clear & ls -alF -h -G'
alias freshrc='source ~/.bashrc'
alias freshpro='source ~/.bash_profile'

alias g='grads'
alias t='tail -f rsl.out.0000'
alias ca='conda_act'
alias caa='conda activate analysis'
alias df='df -h'

alias nc='ncdump -h'
alias topu='top -u nakamura_kento'

alias du='du -h -s'
alias mem='cat /proc/meminfo'
alias cpu='cat /proc/cpuinfo'
alias issue='cat /etc/issue'


export PS1="\[\e[1;32m\]@\h \[\e[1;36m\]\W\\[\e[1;32m\]\\$ \[\e[m\]"


#ulimit -s unlimited

# source /opt/intel/compilers_and_libraries_2019.5.281/linux/bin/compilervars.sh intel64
