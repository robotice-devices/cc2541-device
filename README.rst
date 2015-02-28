
==========
CC2541 BLE
==========

Robotice driver for SensorTag a Bluetooth Low Engery (BLE GATT) device


Requirements
------------

* bluez
* gatttool
* pexpect


Usage
-----

search device MAC

.. code-block:: bash

	hcitool lescan
	LE Scan ...
	78:A5:04:8C:25:A7 (unknown)

get data

.. code-block:: bash

    python cc2541 78:A5:04:8C:25:A7

    in while cycle

    python cc2541 78:A5:04:8C:25:A7 -r


Read More
---------

* based on https://github.com/msaunby/ble-sensor-pi