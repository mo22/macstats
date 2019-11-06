import psutil

print('virtual_memory', psutil.virtual_memory())
print('disk_io_counters', psutil.disk_io_counters(True))
print('cpu_freq', psutil.cpu_freq(True))
print('cpu_percent', psutil.cpu_percent(0, True))

# Cocoa.NSApplication.sharedApplication().setIsAutomaticCustomizeTouchBarMenuItemEnabled(True)  # does not exist`
# Cocoa.NSApplication.sharedApplication().isAutomaticCustomizeTouchBarMenuItemEnabled = True  # read only`



# extension ViewController: NSTouchBarDelegate {
#   override func makeTouchBar() -> NSTouchBar? {
#     // 1
#     let touchBar = NSTouchBar()
#     touchBar.delegate = self
#     // 2
#     touchBar.customizationIdentifier = .travelBar
#     // 3
#     touchBar.defaultItemIdentifiers = [.infoLabelItem]
#     // 4
#     touchBar.customizationAllowedItemIdentifiers = [.infoLabelItem]
#     return touchBar
#   }
# }


# #import <AppKit/AppKit.h>
#
# extern void DFRElementSetControlStripPresenceForIdentifier(NSTouchBarItemIdentifier, BOOL);
# extern void DFRSystemModalShowsCloseBoxWhenFrontMost(BOOL);
#
# @interface NSTouchBarItem ()
#
# + (void)addSystemTrayItem:(NSTouchBarItem *)item;
# + (void)removeSystemTrayItem:(NSTouchBarItem *)item;
#
# @end
#
# @interface NSTouchBar ()
#
# + (void)presentSystemModalTouchBar:(NSTouchBar *)touchBar placement:(long long)placement systemTrayItemIdentifier:(NSTouchBarItemIdentifier)identifier;
# + (void)presentSystemModalTouchBar:(NSTouchBar *)touchBar systemTrayItemIdentifier:(NSTouchBarItemIdentifier)identifier;
# + (void)dismissSystemModalTouchBar:(NSTouchBar *)touchBar;
# + (void)minimizeSystemModalTouchBar:(NSTouchBar *)touchBar;
#
# @end
