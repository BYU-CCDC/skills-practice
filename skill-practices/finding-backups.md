# Finding backups
Tags: offense, backups

## Description
This skill practice is designed to help you find backups on a webserver. Backups are often overlooked by attackers, but they can be a great source of information and can be used to recover from a ransomware attack.

## Goal
Find three backup files on the webserver.

## Setup
1. Download the virtual machine from [https://byu.box.com/s/uxq1x678d01so3ur90io4fd1yvqxnehb](https://byu.box.com/s/uxq1x678d01so3ur90io4fd1yvqxnehb)
2. Import the virtual machine into VirtualBox. Make sure to generate new MAC addresses and set the network adapter to "Host-only mode."
3. Create a snapshot of the virtual machine.
4. Start the virtual machine and log in with the username `root` and the password `backup`.

## Process
1. Run `python /root/hiding_backups.py` to hide the backup files.
2. Find and delete the three backup files on the webserver.

## Rules
* You may not look at the solution located at `/root/backup_locations.txt`.
* You may write scripts (preferable), but they cannot use the solution file either.

## Solution
The three backup file locations are in `/root/backup_locations.txt`.

## Guidance
* Use the command history. Normally, you can use the `history` command. We have made it slightly harder (because of technical difficulties).
* Use the `grep` command. You can use the `grep` command to find lines that match a certain pattern. For example, `grep -r "password" /` will find all lines that contain the word "password" in the entire filesystem.
* Use the `find` command. You can use the `find` command to find files that match a certain pattern. For example, `find / -name "*.txt"` will find all files that end in `.txt`.
* Search for recent files by using the `find` command with the `-mtime` option. For example, `find / -mtime -1` will find all files that have been modified in the last day.

## Cleanup
* Delete `/root/backup_locations.txt`.
* Revert to the snapshot.