#!/bin/bash

set +x
set -e

line="====================================================="
def_target="192.168.112.105"
def_ssh_user="home"
def_ssh_pass="home"
pass_file="password.txt"
mysql_user="root"
mysql_pass="root"

prereq="ssh-copy-id
sshpass
ansible-playbook"

while read -r binary; do
  if ! which "$binary" > /dev/null
  then
    echo -e "'$binary' binary not found.\nNot able to continue.\nPlease contact your admin"
    exit 1
  fi
done <<< "$prereq"

function print_error {
    echo "$@" 1>&2
}

function echo_wlines {
    echo
    echo "<$line"
    echo -e "$1"
    echo "$line>"
}

function read_user_inp {
    chars=$1
    promt="$2"
    read -p "$promt" -n $chars ans
    echo "$ans"
}

function valid_ans {
    ans="$1"
    reg="$2"
    res=$(echo "$ans" | grep -oP "$reg")
    if [[ $? -eq 0 ]]
    then
      echo "$res"
    fi
}

function ask_user {
    chars=$1
    promt="$2"
    reg="$3"
    ans=$(read_user_inp "$chars" "$promt")
    res=$(valid_ans "$ans" "$reg")
    echo "$res"
}

echo_wlines "Welcome to demo app\nThis script will initialize server for the app"
cont=$(ask_user 1 "Continue y/[n]?" "[yY]")
test -z "$cont" && exit 0

echo_wlines "Deploying"
target=$(ask_user 50 "Where to deploy db node? ip or hostname [$def_target]" "[0-9\.a-z\-]+")
test -z "$target" && target="$def_target"
if ping -c1 "$target" >/dev/null
then
  echo "$target is reachable via ICMP"
else
  print_error "$target is NOT reachable via ICMP"
fi
ssh_user=$(ask_user 50 "Enter ssh user name for ansible [$def_ssh_user]:" "[0-9\.a-z_]+")
test -z "$ssh_user" && ssh_user="$def_ssh_user"
ssh_pass=$(ask_user 50 "Enter ssh password for $ssh_user:" "[^ ]+")
test -z "$ssh_pass" && ssh_pass="$def_ssh_pass"
echo "$ssh_pass" > $pass_file
if ! sshpass -f "$pass_file" ssh-copy-id "$ssh_user"@"$target"
then
  rm $pass_file
  print_error "Can't copy your fingerprint to $target.\nNot able to continue.\nPlease contact your admin"
fi
rm $pass_file
echo "it's assumed that mysql credentials are: $mysql_user/$mysql_pass..."
cont=$(ask_user 1 "Do you want to RESET your mysql password y/[n]?" "[yY]")
reset="false"
test -z "$cont" || reset="true"
ansible-playbook --user="$ssh_user" --inventory="$target", --become ansible/db.yml --extra-vars "ansible_sudo_pass=$ssh_pass reset=$reset dbhost=$target"
echo_wlines "Load sharing?"
cnodes=$(ask_user 100 "List GUI IPs for load balancing comma separated? [$target]:" "[0-9\.a-z\-,]+")
test -z "$cnodes" && cnodes="$target"
ansible-playbook --user="$ssh_user" --inventory="$cnodes", --become ansible/deploy.yml --extra-vars "ansible_sudo_pass=$ssh_pass dbhost=$target" --extra-vars="{'cnodes':[$cnodes]}"
