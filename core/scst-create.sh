#!/bin/bash

############              usage:      0              1         2    3      4      5       6
## params ##     ---->>   usage: scst-create local-target-iqn dev group lunNum lvmPath destiqn 
############              usage:  lun begin with 0 <-----------------------|
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
add-target()
{
    echo "add target..."
    $_CMD -add_target $_iqn -driver $_driver
    if [ $? != 0 ] ; then
        error add-target
    fi
}

write-conf()
{
    echo "write conf..."
    $_CMD -write_conf $_conf
    if [ $? != 0 ] ; then
        error write-conf 
    fi
}

enable_target()
{
    echo "enable target..."
    $_CMD -enable_target $_iqn -driver $_driver
    if [ $? != 0 ] ; then
        error enable_target
    fi
}

open-dev()
{
    echo "open dev..."
    #$_CMD -open_dev $_dev -handler $_handler -attributes filename=/dev/raid01434017062/lvm2
    $_CMD -open_dev $_dev -handler $_handler -attributes filename=$_path
    if [ $? != 0 ] ; then
        error open-dev
    fi
}

add-group()
{
    echo "add group..."
    $_CMD -add_group $_group -driver $_driver -target $_iqn
    if [ $? != 0 ] ; then
        error add-group
    fi
}

add-lun()
{
    echo "add lun..."
    $_CMD -add_lun $_lun -driver $_driver -target $_iqn -group $_group -device $_dev
    if [ $? != 0 ] ; then
        error add-lun
    fi
}

add-init()
{
    echo "add init..."
    $_CMD -add_init $_destiqn -driver $_driver -target $_iqn -group $_group
    if [ $? != 0 ] ; then
        error add-init
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
    exit 1
}

usage(){
      echo "*************************************************************************"
      echo "   usage:      0              1         2    3      4      5       6"
      echo "   usage: scst-create local-target-iqn dev group lunNum lvmPath destiqn" 
      echo "   usage:  lun begin with 0 <-----------------------|"
      echo "*************************************************************************"
      
}

create()
{
    add-target
    open-dev
    write-conf
    add-group
    write-conf
    add-lun
    write-conf
    add-init
    write-conf
    enable_target
    write-conf
}


## kill the Daemon program
pkill Daemon
#if [ $? != 0 ]; then
#    echo "Error: Daemon not stopped.. Exit"
#    exit 1
#fi

#sleep 10

if [ $1 = "-h" ] ; then
    usage
    exit 0
fi


create
