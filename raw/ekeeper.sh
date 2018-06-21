#!/bin/sh
echo "Updating /etc/ekeeper.list and /etc/installed.list"
dnf list --installed  | tail -n+2 |  sort > /etc/installed.list
etckeeper list-installed | sort > /etc/ekeeper.list
