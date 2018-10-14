from construct import Struct, UBInt8

FrameData = Struct("FrameData",
    UBInt8("GetState"),
    UBInt8("State"),
    UBInt8("Dimmer")
)
