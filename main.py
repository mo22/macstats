import io
import traceback

import sensors
import touchbar

import AppKit
import PyObjCTools.AppHelper
import objc

from PIL import Image, ImageDraw, ImageFont

from typing import Dict, Optional


class AppDelegate(AppKit.NSObject):
    timer: AppKit.NSTimer
    sensor = sensors.PsUtilSensor()
    statusItems: Dict[str, AppKit.NSStatusItem] = {}
    cpuWarningsMenu: Optional[AppKit.NSMenu] = None

    @objc.python_method
    def pilToNSImage(self, img):
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
    def updateCpuWarningsMenu(self) -> None:
        statusItem = self.addStatusItem('cpu_percent')
        if self.cpuWarningsMenu is None:
            self.cpuWarningsMenu = AppKit.NSMenu.alloc().initWithTitle_('')
        self.cpuWarningsMenu.removeAllItems()
        for proc in self.sensor.get_processes_by_cpu():
            if proc.cpu_percent < 5:
                break
            self.cpuWarningsMenu.addItem_(
                AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    f"{proc.cpu_percent:.0f}% {proc.process.name()}", None, ''
                )
            )
        statusItem.setMenu_(self.cpuWarningsMenu)

    @objc.python_method
    def updateCpuWarnings(self) -> None:
        if self.sensor.get_cpu_percent_max() > 75:
            statusItem = self.addStatusItem('cpu_percent')
            statusItem.setTitle_(f"cpu max {self.sensor.get_cpu_percent_max():.0f} %")
            self.updateCpuWarningsMenu()
        else:
            if self.sensor.get_cpu_percent_avg() > 75:
                statusItem = self.addStatusItem('cpu_percent')
                statusItem.setTitle_(f"cpu avg {self.sensor.get_cpu_percent_avg():.0f} %")
                self.updateCpuWarningsMenu()
            else:
                self.removeStatusItem('cpu_percent')

    @objc.python_method
    def updateDiskWarnings(self) -> None:
        dev = self.sensor.get_disk_dev_most_active()
        if dev:
            read = self.sensor.get_disk_read_bytes_per_sec(dev)
            write = self.sensor.get_disk_write_bytes_per_sec(dev)
            if write > 1024 * 1024:
                statusItem = self.addStatusItem('disk')
                statusItem.setTitle_(f"{dev} write {(write / 1024 / 1024):.0f} MB/s")
            elif read > 1024 * 1024:
                statusItem = self.addStatusItem('disk')
                statusItem.setTitle_(f"{dev} read {(read / 1024 / 1024):.0f} MB/s")
            else:
                self.removeStatusItem('disk')
        else:
            self.removeStatusItem('disk')

    @objc.python_method
    def updateNetWarnings(self) -> None:
        dev = self.sensor.get_net_dev_most_active()
        if dev:
            recv = self.sensor.get_net_recv_bytes_per_sec(dev)
            sent = self.sensor.get_net_sent_bytes_per_sec(dev)
            if recv > 1024 * 1024:
                statusItem = self.addStatusItem('net')
                statusItem.setTitle_(f"{dev} recv {(recv / 1024 / 1024 * 8):.0f} MBit/s")
            elif sent > 1024 * 1024:
                statusItem = self.addStatusItem('net')
                statusItem.setTitle_(f"{dev} sent {(sent / 1024 / 1024 * 8):.0f} MBit/s")
            else:
                self.removeStatusItem('net')
        else:
            self.removeStatusItem('net')

    def applicationDidFinishLaunching_(self, notification):
        try:
            self.timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                0.5,
                self,
                'onTimer',
                None,
                True
            )
        except Exception:
            traceback.print_exc()

    def onTimer(self) -> None:
        try:
            self.sensor.refresh()
            self.updateCpuWarnings()
            self.updateDiskWarnings()
            self.updateNetWarnings()
            self.updateTouchbar()
        except Exception:
            traceback.print_exc()

    def onQuit(self) -> None:
        try:
            AppKit.NSApplication.sharedApplication().terminate_(None)
        except Exception:
            traceback.print_exc()

    touchBarItem: Optional[AppKit.NSCustomTouchBarItem] = None
    touchBarButton: Optional[AppKit.NSButton] = None

    def onTouchBarButton(self) -> None:
        AppKit.NSWorkspace.sharedWorkspace().launchApplication_('/System/Applications/Utilities/Activity Monitor.app')

    @objc.python_method
    def updateTouchbar(self) -> None:
        if not self.touchBarItem:
            touchbar.DFRSystemModalShowsCloseBoxWhenFrontMost(True)
            self.touchBarItem = AppKit.NSCustomTouchBarItem.alloc().initWithIdentifier_(
                'test'
            )
            img = Image.new('RGBA', (120, 48), color='#00000000')
            self.touchBarButton = AppKit.NSButton.buttonWithImage_target_action_(
                self.pilToNSImage(img), self, 'onTouchBarButton'
            )
            self.touchBarItem.setView_(self.touchBarButton)
            AppKit.NSTouchBarItem.addSystemTrayItem_(self.touchBarItem)
            touchbar.DFRElementSetControlStripPresenceForIdentifier('test', True)

        cpu_max = self.sensor.get_cpu_percent_max()
        cpu_avg = self.sensor.get_cpu_percent_avg()
        img = Image.new('RGBA', (120, 48), color='#00000000')
        font = ImageFont.truetype('Avenir.ttc', 22)
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), f"CPU {int(cpu_max)} {int(cpu_avg)}", fill='#ffffff', font=font)
        del draw
        del font
        self.touchBarButton.setImage_(self.pilToNSImage(img))


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
