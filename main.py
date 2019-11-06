import AppKit
import PyObjCTools.AppHelper
import traceback


class AppDelegate(AppKit.NSObject):
    def onquit_(self, nsmenuitem):
        print("onquit_")
        AppKit.NSApplication.sharedApplication().terminate_(None)

    def ontest_(self, nsmenuitem):
        try:
            print("ontest_", nsmenuitem)
        except Exception:
            traceback.print_exc()

    def onblah_(self, nsmenuitem):
        try:
            print("onblah_", nsmenuitem)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':

    appDelegate = AppDelegate.alloc().init()
    app = AppKit.NSApplication.sharedApplication()
    app.activateIgnoringOtherApps_(True)
    # AppKit.NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_(appDelegate)
    app.setDelegate_(appDelegate)

    statusItem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
    statusItem.setTitle_('Hello')

    menu = AppKit.NSMenu.alloc().initWithTitle_("Menu")
    statusItem.setMenu_(menu)

    menuItem1 = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Test", None, '')
    menuItem1.setTarget_(appDelegate)
    menuItem1.setAction_('ontest:')
    menu.addItem_(menuItem1)

    menuItem1 = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Blah", None, '')
    menuItem1.setTarget_(appDelegate)
    menuItem1.setAction_('onblah:')
    menu.addItem_(menuItem1)

    menuItem1 = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
        "Quit", None, '')
    menuItem1.setTarget_(appDelegate)
    menuItem1.setAction_('onquit:')
    menu.addItem_(menuItem1)

    PyObjCTools.AppHelper.installMachInterrupt()
    PyObjCTools.AppHelper.runEventLoop()
