import io
import traceback

import sensors
import touchbar

import AppKit
import PyObjCTools.AppHelper
import objc

from PIL import Image, ImageDraw, ImageFont

from typing import Dict


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


# protocols=[objc.protocolNamed('NSApplicationDelegate')] ?
class AppDelegate(AppKit.NSObject):
    timer: AppKit.NSTimer
    sensor = sensors.PsUtilSensor()
    statusItems: Dict[str, AppKit.NSStatusItem] = {}

    @objc.python_method
    def addStatusItem(self, name: str) -> AppKit.NSStatusItem:
        statusItem = self.statusItems.get(name, None)
        if statusItem is None:
            statusItem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
            self.statusItems[name] = statusItem
        return statusItem

    @objc.python_method
    def removeStatusItem(self, name: str) -> None:
        self.statusItems.pop(name, None)

    @objc.python_method
    def updateWarnings(self) -> None:
        if True:
            if self.sensor.get_cpu_percent_avg() > 75:
                statusItem = self.addStatusItem('cpu_percent_avg')
                statusItem.setTitle_(f"Avg Cpu: {self.sensor.get_cpu_percent_avg():.0f}%")
            else:
                self.removeStatusItem('cpu_percent_avg')
        if True:
            if self.sensor.get_cpu_percent_max() > 75:
                pass

    # @objc.python_method
    # def updateImage(self):
    #     cpu_max = psUtilSensor.get_cpu_percent_max()
    #     cpu_avg = psUtilSensor.get_cpu_percent_avg()
    #     img = Image.new('RGBA', (120, 48), color='#00000000')
    #     # font = ImageFont.truetype('Arial Unicode.ttf', 22)
    #     font = ImageFont.truetype('Avenir.ttc', 22)
    #     draw = ImageDraw.Draw(img)
    #     draw.text((0, 0), f"CPU {int(cpu_max)} {int(cpu_avg)}", fill='#000000', font=font)
    #     del draw
    #     del font
    #     self.statusItem.setImage_(pilToNSImage(img))

    def applicationDidFinishLaunching_(self, notification):
        try:
            self.timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                0.5,
                self,
                'onTimer',
                None,
                True
            )

            self.statusItem = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
            self.statusItem.setTitle_('Hello')
            menu = AppKit.NSMenu.alloc().initWithTitle_("Menu")
            self.statusItem.setMenu_(menu)
            menuItem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                "Quit", None, '')
            menuItem.setTarget_(appDelegate)
            menuItem.setAction_('onQuit')
            menu.addItem_(menuItem)

            # touchbar.DFRSystemModalShowsCloseBoxWhenFrontMost(True)
            # self.touchBarItem = AppKit.NSCustomTouchBarItem.alloc().initWithIdentifier_(
            #     'test'
            # )
            # img = Image.new('RGBA', (120, 48), color='#00000000')
            # font = ImageFont.truetype('Avenir.ttc', 44)
            # draw = ImageDraw.Draw(img)
            # draw.text((0, 0), f"Hello", fill='#ff00ff', font=font)
            # del draw
            # del font
            # button = AppKit.NSButton.buttonWithImage_target_action_(
            #     pilToNSImage(img), self, 'onquit'
            # )
            # # button = AppKit.NSButton.buttonWithTitle_target_action_(
            # #     'XX', self, 'onquit'
            # # )
            # self.touchBarItem.setView_(button)
            # AppKit.NSTouchBarItem.addSystemTrayItem_(self.touchBarItem)
            # touchbar.DFRElementSetControlStripPresenceForIdentifier('test', True)
        except Exception:
            traceback.print_exc()

    def onTimer(self):
        try:
            self.sensor.refresh()
            # self.updateImage()
            # print('virtual_memory', psutil.virtual_memory())
            # print('disk_io_counters', psutil.disk_io_counters(True))
            # print('net_io_counters', psutil.net_io_counters(True))
            # print('cpu_freq', psutil.cpu_freq(True))
            # print('cpu_percent', psutil.cpu_percent(0, True))
            # img = Image.new('RGBA', (120, 48), color='#00000000')
            # font = ImageFont.truetype('Avenir.ttc', 44)
            # draw = ImageDraw.Draw(img)
            # draw.text((0, 0), f"NEW", fill='#ff00ff', font=font)
            # del draw
            # del font
            # self.touchBarItem.view().setImage_(pilToNSImage(img))
        except Exception:
            traceback.print_exc()

    def onQuit(self):
        try:
            print('AppDelegate.onQuit')
            AppKit.NSApplication.sharedApplication().terminate_(None)
        except Exception:
            traceback.print_exc()



if __name__ == '__main__':
    appDelegate = AppDelegate.alloc().init()

    app = AppKit.NSApplication.sharedApplication()
    app.setDelegate_(appDelegate)
    app.activateIgnoringOtherApps_(True)

    # hide from dock
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

    # handle ctrl-c
    PyObjCTools.AppHelper.installMachInterrupt()

    PyObjCTools.AppHelper.runEventLoop()
