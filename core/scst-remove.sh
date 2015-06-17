#!/bin/bash

############              usage:      0              1         2    3      4      5       6
## params ##     ---->>   usage: scst-remove local-target-iqn dev group lunNum lvmPath destiqn 
###########
_iqn=$1
_dev=$2
_group=$3
_lun=$4
_path=$5
_destiqn=$6

_driver=iscsi
_handler=vdisk_blockio
_conf=/etc/scst.conf

_CMD=scstadmin


#################
## func define ##
#################
close-dev()
{
    echo "open dev..."
    echo "y" | $_CMD -close_dev $_dev -handler $_handler -attributes filename=$_path 
    if [ $? != 0 ] ; then
        error close-dev
    fi
}

remove-init()
{
    echo "remove init..."
    echo "y" | $_CMD -rem_init $_destiqn -driver $_driver -target $_iqn -group $_group
    if [ $? != 0 ] ; then
        error remove-init
    fi
}

remove-lun()
{
    echo "remove lun..."
    echo "y" | $_CMD -rem_lun $_lun -driver $_driver -target $_iqn -group $_group -device $_dev
    if [ $? != 0 ] ; then
        error remove-lun
    fi
}

remove-group()
{
    echo "remove group..."
    echo "y" | $_CMD -rem_group $_group -driver $_driver -target $_iqn
    if [ $? != 0 ] ; then
        error remove-group
    fi
}

disable-target()
{
    echo "disable target..."
    echo "y" | $_CMD -disable_target $_iqn -driver $_driver
    if [ $? != 0 ] ; then
        error disable-target
    fi
}

remove-target()
{
    echo "remove target..."
    echo "y" | $_CMD -rem_target $_iqn -driver $_driver
    if [ $? != 0 ] ; then
        error remove-target
    fi
}



check-result()
{
    if [ $? != 0 ] ; then
        error $1
    fi
}

error()
{
    echo "Error: $1...Exit"
    #exit 1
}

remove()
{
    remove-lun
    close-dev
    remove-init
    remove-group
    disable-target
    remove-target
}

## kill the Daemon program
#pkill Daemon
#if [ $? != 0 ]; then
#    echo "Error: Daemon not stopped.. Exit"
#    exit 1
#fi

remove
