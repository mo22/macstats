import AppKit
import PyObjCTools.AppHelper
import traceback


class AppDelegate(AppKit.NSObject):
    def applicationDidFinishLaunching_(self, notification):
        print('AppDelegate.applicationDidFinishLaunching')
        self.statusItem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
        self.statusItem.setTitle_('Hello')
        # self.systray_item.button().setImage_(icon_load('icons/tray_error.png'))
        # res = AppKit.NSImage.alloc().initWithContentsOfFile_(name)
        # <key>LSUIElement</key>
        # <true/>

        menu = AppKit.NSMenu.alloc().initWithTitle_("Menu")
        self.statusItem.setMenu_(menu)

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

    def onquit_(self, nsmenuitem):
        print("onquit_")
        AppKit.NSApplication.sharedApplication().terminate_(None)

    # def systray_setup(self):
    #   self.systray_item = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
    #   self.systray_item.button().setImage_(icon_load('icons/tray_error.png'))
    #   self.systray_menu = AppKit.NSMenu.alloc().initWithTitle_("Menu")
    #   self.systray_menu.setDelegate_(self)
    #   self.systray_item.setMenu_(self.systray_menu)
    #   self.systray_labelView = None
    #   self.systray_timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
    #     0.5, action_selector(lambda: self.systray_refresh()), 'action', None, True)
    #

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
    app.setDelegate_(appDelegate)
    app.activateIgnoringOtherApps_(True)
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
    PyObjCTools.AppHelper.installMachInterrupt()
    PyObjCTools.AppHelper.runEventLoop()
