import io
import traceback
import time
import math

import sensors
# import touchbar

import AppKit
import PyObjCTools.AppHelper
import objc

from PIL import Image, ImageOps

from typing import Dict, Optional


def pil_to_nsimage(img: Image, scale=0.5):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    nsimg = AppKit.NSImage.alloc().initWithData_(
        AppKit.NSData.dataWithBytes_length_(
            buf.getvalue(), len(buf.getvalue())
        )
    )
    del buf
    nsimg.setSize_((int(img.size[0] * scale), int(img.size[1] * scale)))
    return nsimg


def tint_image(img: Image, color: str) -> Image:
    # hum?
    r, g, b, alpha = img.split()
    res = ImageOps.colorize(r, color, color)
    res.putalpha(alpha)
    return res


class MovingAverage:
    seconds: float
    time: float = 0
    value: Optional[float] = None

    def __init__(self, seconds: float):
        self.seconds = seconds

    def __call__(self, value: float) -> float:
        t = time.time()
        if self.value is None or (t - self.time) > 3600:
            self.value = value
        elif value == 0:
            self.value = value
        else:
            exp = 1.0 / math.exp((t - self.time) / self.seconds)
            self.value = (self.value * exp) + (value * (1 - exp))
        self.time = t
        return self.value


class AppDelegate(AppKit.NSObject):
    timer: AppKit.NSTimer
    sensor = sensors.PsUtilSensor()
    status_items: Dict[str, AppKit.NSStatusItem] = {}
    cpu_warnings_menu: Optional[AppKit.NSMenu] = None

    ema_disk_read = MovingAverage(0.5)
    ema_disk_write = MovingAverage(0.5)
    ema_net_sent = MovingAverage(0.5)
    ema_net_recv = MovingAverage(0.5)

    icon_menu: Optional[AppKit.NSMenu] = None
    icon_base = Image.open('activity.png')
    icon_idle = pil_to_nsimage(Image.open('activity.png'))
    icon_red = pil_to_nsimage(tint_image(icon_base, 'red'))
    icon_orange = pil_to_nsimage(tint_image(icon_base, 'orange'))

    @objc.python_method
    def add_status_item(self, name: str) -> AppKit.NSStatusItem:
        status_item = self.status_items.get(name, None)
        if status_item is None:
            status_item = AppKit.NSStatusBar.systemStatusBar().statusItemWithLength_(-1)
            self.status_items[name] = status_item
        return status_item

    @objc.python_method
    def remove_status_item(self, name: str) -> None:
        self.status_items.pop(name, None)

    @objc.python_method
    def update_cpu_warnings_menu(self) -> None:
        status_item = self.add_status_item('cpu_percent')
        if self.cpu_warnings_menu is None:
            self.cpu_warnings_menu = AppKit.NSMenu.alloc().initWithTitle_('')
        self.cpu_warnings_menu.removeAllItems()
        for proc in self.sensor.get_processes_by_cpu():
            if proc.cpu_percent < 5:
                break
            self.cpu_warnings_menu.addItem_(
                AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    f"{proc.cpu_percent:.0f}% {proc.name}", None, ''
                )
            )
        status_item.setMenu_(self.cpu_warnings_menu)

    @objc.python_method
    def update_cpu_warnings(self) -> None:
        status_item = None
        if self.sensor.get_cpu_percent_max() > 75:
            status_item = self.add_status_item('cpu_percent')
            status_item.setTitle_(f"cpu max {self.sensor.get_cpu_percent_max():.0f} %")
            self.update_cpu_warnings_menu()
        elif self.sensor.get_cpu_percent_avg() > 75:
            status_item = self.add_status_item('cpu_percent')
            status_item.setTitle_(f"cpu avg {self.sensor.get_cpu_percent_avg():.0f} %")
            self.update_cpu_warnings_menu()
        elif self.sensor.get_cpu_percent_top() > 50:
            status_item = self.add_status_item('cpu_percent')
            status_item.setTitle_(f"cpu top {self.sensor.get_cpu_percent_top():.0f} %")
            self.update_cpu_warnings_menu()
        else:
            self.remove_status_item('cpu_percent')

    @objc.python_method
    def update_disk_warnings(self) -> None:
        status_item = None
        dev = self.sensor.get_disk_dev_most_active()
        read = self.ema_disk_read(self.sensor.get_disk_read_bytes_per_sec(dev) if dev else 0)
        write = self.ema_disk_write(self.sensor.get_disk_write_bytes_per_sec(dev) if dev else 0)
        if write > 1024 * 1024 and write > read:
            status_item = self.add_status_item('disk')
            status_item.setTitle_(f"{dev} write {(write / 1024 / 1024):.0f} MB/s")
        elif read > 1024 * 1024:
            status_item = self.add_status_item('disk')
            status_item.setTitle_(f"{dev} read {(read / 1024 / 1024):.0f} MB/s")
        else:
            self.remove_status_item('disk')
        # if status_item:
        #     status_item.setTarget_(self)
        #     status_item.setAction_('onTouchBarButton')

    @objc.python_method
    def update_net_warnings(self) -> None:
        status_item = None
        dev = self.sensor.get_net_dev_most_active()
        # EMA
        recv = self.ema_net_recv(self.sensor.get_net_recv_bytes_per_sec(dev) if dev else 0)
        sent = self.ema_net_sent(self.sensor.get_net_sent_bytes_per_sec(dev) if dev else 0)
        if recv > 1024 * 1024 and recv > sent:
            status_item = self.add_status_item('net')
            status_item.setTitle_(f"{dev} recv {(recv / 1024 / 1024 * 8):.0f} MBit/s")
        elif sent > 1024 * 1024:
            status_item = self.add_status_item('net')
            status_item.setTitle_(f"{dev} sent {(sent / 1024 / 1024 * 8):.0f} MBit/s")
        else:
            self.remove_status_item('net')
        # if status_item:
        #     status_item.setTarget_(self)
        #     status_item.setAction_('onTouchBarButton')

    @objc.python_method
    def update_icon(self) -> None:
        status_item = self.add_status_item('main')
        icon = self.icon_idle

        if self.icon_menu is None:
            self.icon_menu = AppKit.NSMenu.alloc().initWithTitle_('')
        self.icon_menu.removeAllItems()

        if True:
            dev = self.sensor.get_disk_dev_most_active()
            read = self.ema_disk_read(self.sensor.get_disk_read_bytes_per_sec(dev) if dev else 0)
            write = self.ema_disk_write(self.sensor.get_disk_write_bytes_per_sec(dev) if dev else 0)
            if read > 1024 * 1024:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"{dev} read {(read / 1024 / 1024):.0f} MB/s", None, ''
                    )
                )
                icon = self.icon_orange
            if write > 1024 * 1024:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"{dev} write {(write / 1024 / 1024):.0f} MB/s", None, ''
                    )
                )
                icon = self.icon_orange

        if True:
            dev = self.sensor.get_net_dev_most_active()
            recv = self.ema_net_recv(self.sensor.get_net_recv_bytes_per_sec(dev) if dev else 0)
            sent = self.ema_net_sent(self.sensor.get_net_sent_bytes_per_sec(dev) if dev else 0)
            if recv > 1024 * 1024:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"{dev} recv {(recv / 1024 / 1024 * 8):.0f} MBit/s", None, ''
                    )
                )
                icon = self.icon_orange
            if sent > 1024 * 1024:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"{dev} sent {(sent / 1024 / 1024 * 8):.0f} MBit/s", None, ''
                    )
                )
                icon = self.icon_orange

        if True:
            if self.sensor.get_cpu_percent_top() > 50:
                icon = self.icon_orange
            if self.sensor.get_cpu_percent_max() > 75:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"CPU Core {self.sensor.get_cpu_percent_max():.0f}%", None, ''
                    )
                )
                icon = self.icon_red
            if self.sensor.get_cpu_percent_avg() > 75:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"CPU Total {self.sensor.get_cpu_percent_avg():.0f}%", None, ''
                    )
                )
                icon = self.icon_red

        if True:
            if self.sensor.virtual_memory.percent > 80:
                self.icon_menu.addItem_(
                    AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                        f"Memory {self.sensor.virtual_memory.percent:.0f}%", None, ''
                    )
                )
            if self.sensor.virtual_memory.percent > 90:
                icon = self.icon_red

        self.icon_menu.addItem_(
            AppKit.NSMenuItem.separatorItem()
        )

        for proc in self.sensor.get_processes_by_cpu():
            if proc.cpu_percent < 5:
                break
            self.icon_menu.addItem_(
                AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                    f"{proc.cpu_percent:.0f}% {proc.name}", None, ''
                )
            )

        self.icon_menu.addItem_(
            AppKit.NSMenuItem.separatorItem()
        )

        self.icon_menu.addItem_(
            AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                'Quit', 'onQuit', ''
            )
        )

        status_item.setMenu_(self.icon_menu)
        status_item.setImage_(icon)

    def applicationDidFinishLaunching_(self, notification):
        try:
            self.timer = AppKit.NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
                2,
                self,
                'onTimer',
                None,
                True
            )
            AppKit.NSRunLoop.mainRunLoop().addTimer_forMode_(self.timer, AppKit.NSRunLoopCommonModes)
            self.update_icon()
        except Exception:
            traceback.print_exc()

    def onTimer(self) -> None:
        try:
            self.sensor.refresh()
            # self.update_cpu_warnings()
            # self.update_disk_warnings()
            # self.update_net_warnings()
            # self.update_touchbar()
            self.update_icon()
        except Exception:
            traceback.print_exc()

    def onQuit(self) -> None:
        try:
            AppKit.NSApplication.sharedApplication().terminate_(None)
        except Exception:
            traceback.print_exc()

    # touchbar_item: Optional[AppKit.NSCustomTouchBarItem] = None
    # touchbar_button: Optional[AppKit.NSButton] = None
    #
    # def onTouchBarButton(self) -> None:
    #     AppKit.NSWorkspace.sharedWorkspace().launchApplication_('/System/Applications/Utilities/Activity Monitor.app')
    #
    # @objc.python_method
    # def update_touchbar(self) -> None:
    #     if not self.touchbar_item:
    #         touchbar.DFRSystemModalShowsCloseBoxWhenFrontMost(True)
    #         self.touchbar_item = AppKit.NSCustomTouchBarItem.alloc().initWithIdentifier_(
    #             'test'
    #         )
    #         img = Image.new('RGBA', (120, 48), color='#00000000')
    #         self.touchbar_button = AppKit.NSButton.buttonWithImage_target_action_(
    #             pil_to_nsimage(img), self, 'onTouchBarButton'
    #         )
    #         self.touchbar_item.setView_(self.touchbar_button)
    #         AppKit.NSTouchBarItem.addSystemTrayItem_(self.touchbar_item)
    #         touchbar.DFRElementSetControlStripPresenceForIdentifier('test', True)
    #
    #     cpu_max = self.sensor.get_cpu_percent_max()
    #     cpu_avg = self.sensor.get_cpu_percent_avg()
    #     img = Image.new('RGBA', (120, 48), color='#00000000')
    #     font = ImageFont.truetype('Avenir.ttc', 22)
    #     draw = ImageDraw.Draw(img)
    #     draw.text((0, 0), f"CPU {int(cpu_max)} {int(cpu_avg)}", fill='#ffffff', font=font)
    #     del draw
    #     del font
    #     self.touchbar_button.setImage_(pil_to_nsimage(img))


if __name__ == '__main__':
    app_delegate = AppDelegate.alloc().init()

    app = AppKit.NSApplication.sharedApplication()
    app.setDelegate_(app_delegate)
    app.activateIgnoringOtherApps_(True)

    # hide from dock
    app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

    # handle ctrl-c
    PyObjCTools.AppHelper.installMachInterrupt()

    PyObjCTools.AppHelper.runEventLoop()
