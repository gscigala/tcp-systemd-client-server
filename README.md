# tcp-systemd-client-server
TCP client/server managing systemd service

## Protocol

Frame description

----------------------------------------------------------------
|     bit     | 23             16|15           8|7            0|
----------------------------------------------------------------
|  Variable   |        State     |   GetState   |    Dimmer    |
----------------------------------------------------------------

* State 
  * 1: enable service, 
  * O: disable service
* GetState
  * 1: return service state, 
  * 0: not return service state 
* Dimmer 
  * Value of the power to assign: 0 to 100, 255 if not used.
