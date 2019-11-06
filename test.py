# noqa: E501
# flake8: noqa
# :PEP8 -E501
# pep8: disable=E501
# noqa: ignore=E501
# flake8: ignore=F403,E501

import Cocoa  # pip install pyobjc-framework-cocoa
import PyObjCTools.AppHelper
# import AppKit
import psutil  # pip install psutil



# print(Cocoa.NSTouchBarItem)  # works`
# print(Cocoa.NSTouchBarItem.addSystemTrayItem)  # does not work

# print('virtual_memory', psutil.virtual_memory())
#
# print('disk_io_counters', psutil.disk_io_counters(True))
#
# print('cpu_freq', psutil.cpu_freq(True))
#
# print('cpu_percent', psutil.cpu_percent(0, True))
#
#
# app = Cocoa.NSApplication.sharedApplication()
# print('app', app)

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


# Initiate the contrller with a XIB
# viewController = SimpleXibDemoController.alloc().initWithWindowNibName_("SimpleXibDemo")

# Show the window
# viewController.showWindow_(viewController)

# Bring app to top
# Cocoa.NSApp.activateIgnoringOtherApps_(True)

# PyObjCTools.AppHelper.runEventLoop()
