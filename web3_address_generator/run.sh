#!/bin/bash

set -e

python web3_address_generator.py \
--address-start 0000 aaaa bbbb cccc dddd eeee ffff bbc0c 6900 6969 \
--address-end 0000 0069 6969 aaaa bbbb cccc dddd eeee ffff \
--number-of-addresses 10