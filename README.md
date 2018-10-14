# tcp-systemd-client-server
TCP client/server managing systemd service

## Protocol

Frame description

----------------------------------------------------------------
|     bit     |0 7|8 15|16 23|
----------------------------------------------------------------
|  Variable   |     GetState     |     State    |    Dimmer    |
----------------------------------------------------------------

* GetState
  * 1: return service state, 
  * 0: not return service state 
* State 
  * 1: enable service, 
  * O: disable service
* Dimmer 
  * Value of the power to assign: 0 to 100, 255 if not used.
