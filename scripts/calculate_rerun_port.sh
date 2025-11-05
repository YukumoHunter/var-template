#!/bin/sh

ROS_DOMAIN_ID=$(( ${ROS_DOMAIN_ID} ))
if [ $ROS_DOMAIN_ID -lt 10 ]; then
    RERUN_PORT="1000${ROS_DOMAIN_ID}"
else
    RERUN_PORT="100${ROS_DOMAIN_ID}"
fi

echo $RERUN_PORT
