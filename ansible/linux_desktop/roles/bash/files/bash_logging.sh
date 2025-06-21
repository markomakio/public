export HISTTIMEFORMAT="%F %T %Z "
export HISTSIZE=10000
export HISTFILESIZE=10000
PORT=$(who am i | awk '{ print $5 }' | tr -d "[()]")
logger -p local6.notice -t "bash $LOGNAME $$" User $LOGNAME logged from $PORT
function history_to_syslog
{
  declare cmd
  declare p_dir
  declare LOG_NAME
  cmd=$(HISTTIMEFORMAT="" history 1)
  cmd=$(echo $cmd |awk '{print substr($0,length($1)+2)}')
  p_dir=$(pwd)
  if [ "$cmd" != "$old_command" ]; then
      logger -p local6.notice -- SESSION = $$, from_remote_host = $PORT,  USER = $(logname)/$(whoami),  PWD = $p_dir, CMD = "${cmd}"
  fi
  old_command=$cmd
}
trap history_to_syslog DEBUG || EXIT
