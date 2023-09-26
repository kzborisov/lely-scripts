#!/bin/bash

usage="$(basename "$0") [-h] [-p] [-u] -- change the Recovery Updater CLI on the runners

where:
    -p  local path to the Recovery Updater
    -u  the user on the runner"



unset -v path_to_ru
unset -v user

while getopts h:p:u: opt; do
        case $opt in
                p) path_to_ru=$OPTARG ;;
                u) user=$OPTARG ;;
                *)
                    echo "$usage" >&2
                    exit 1
        esac
done

shift "$(( OPTIND - 1 ))"

if [ -z "$path_to_ru" ] || [ -z "$user" ]; then
        echo 'Missing -p or -u' >&2
        echo "$usage"
        exit 1
fi


function replaceAndChangeOwner {
    echo "Copying to $user@$1"
    rsync --progress "$path_to_ru" "$user"@"$1":/home/lely/offline_updater/extras/
    ssh "$user"@"$1" sudo chown -R lely:lely /home/lely/offline_updater/extras/
}


replaceAndChangeOwner "192.168.100.61"
replaceAndChangeOwner "192.168.100.62"
replaceAndChangeOwner "192.168.100.63"
replaceAndChangeOwner "192.168.100.64"
replaceAndChangeOwner "192.168.100.71"
replaceAndChangeOwner "192.168.100.72"
replaceAndChangeOwner "192.168.100.73"
replaceAndChangeOwner "192.168.100.74"

echo "Done!"
