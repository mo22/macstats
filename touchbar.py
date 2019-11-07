import AppKit
import objc

AppKit.NSTouchBarItem

scope = {}
objc.objc.loadBundleFunctions(
    None,
    scope,
    [
        ('DFRElementSetControlStripPresenceForIdentifier', objc._C_VOID + objc._C_ID + objc._C_BOOL),
        ('DFRSystemModalShowsCloseBoxWhenFrontMost', objc._C_VOID + objc._C_BOOL),
    ]
)

DFRElementSetControlStripPresenceForIdentifier = scope['DFRElementSetControlStripPresenceForIdentifier']
DFRSystemModalShowsCloseBoxWhenFrontMost = scope['DFRSystemModalShowsCloseBoxWhenFrontMost']
