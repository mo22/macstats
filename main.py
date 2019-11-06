import AppKit
import PyObjCTools.AppHelper
import traceback
from PIL import Image, ImageDraw, ImageFont
import io


def pilToNSImage(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    nsimg = AppKit.NSImage.alloc().initWithData_(
        AppKit.NSData.dataWithBytes_length_(
            buf.getvalue(), len(buf.getvalue())
        )
    )
    del buf
    nsimg.setSize_((img.size[0] / 2, img.size[1] / 2))
    return nsimg


class AppDelegate(AppKit.NSObject):
    def updateImage(self):
        img = Image.new('RGBA', (48, 48), color='#00000000')
        # font = ImageFont.truetype('Arial Unicode.ttf', 22)
        font = ImageFont.truetype('Avenir.ttc', 22)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), '99', fill='#000000', font=font)
        del draw
        del font
        self.statusItem.setImage_(pilToNSImage(img))

    def applicationDidFinishLaunching_(self, notification):
        print('AppDelegate.applicationDidFinishLaunching')

        self.statusItem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
        # self.statusItem.setTitle_('Hello')
        self.updateImage()

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