import threading
import asyncio
import time
import tkinter as tk
from tkinter import ttk
from station import Station

class ControlWindow:
    def __init__(self, root):
        root.title("Rexair Automation Software Updater")
        root.geometry("800x400")
        
        # Main container frames
        self.left_frame = tk.Frame(root)
        self.right_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # --- Right Frame: Stations ---
        self.right_frame_label = tk.LabelFrame(self.right_frame, text="Stations")
        self.right_frame_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.station_button = tk.Button(self.right_frame_label, text="Update", width=10)
        self.station_button.pack(pady=(20,10))

        self.check_vars_right = []
        for i in range(7):
            var = tk.IntVar()
            cb = tk.Checkbutton(self.right_frame_label, text="Boot", variable=var,
                                command=lambda v=var, cb_index=i: self.toggle_checkbox(v, cb_index, side="right"))
            cb.pack(anchor="center", pady=2)
            self.check_vars_right.append((var, cb))

        # --- Left Frame: Top and Bottom ---
        self.top_left = tk.LabelFrame(self.left_frame, text="Interface Controller")
        self.bottom_left = tk.LabelFrame(self.left_frame, text="System Controller")
        self.top_left.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.bottom_left.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Top left: IP Entry and Update + Checkbox
        self.ip_entry = tk.Entry(self.top_left)
        self.ip_entry.insert(0, "192.168.0.1")
        self.ip_entry.pack(pady=(10,5))

        self.top_update_var = tk.IntVar()
        top_update_frame = tk.Frame(self.top_left)
        top_update_frame.pack(pady=5)
        self.top_update_btn = tk.Button(top_update_frame, text="Update", width=10)
        self.top_update_btn.pack(side=tk.LEFT)
        self.top_update_cb = tk.Checkbutton(top_update_frame, text="Boot", variable=self.top_update_var,
                                            command=lambda: self.toggle_checkbox(self.top_update_var, 0, side="left_top"))
        self.top_update_cb.pack(side=tk.LEFT, padx=5)

        # Bottom left: Update + Checkbox
        self.bottom_update_var = tk.IntVar()
        bottom_update_frame = tk.Frame(self.bottom_left)
        bottom_update_frame.pack(pady=20)
        self.bottom_update_btn = tk.Button(bottom_update_frame, text="Update", width=10)
        self.bottom_update_btn.pack(side=tk.LEFT)
        self.bottom_update_cb = tk.Checkbutton(bottom_update_frame, text="Boot", variable=self.bottom_update_var,
                                               command=lambda: self.toggle_checkbox(self.bottom_update_var, 0, side="left_bottom"))
        self.bottom_update_cb.pack(side=tk.LEFT, padx=5)

    def toggle_checkbox(self, var, index, side):
        """Update checkbox text based on value"""
        text = "Boot" if var.get() else "Main"
        if side == "right":
            self.check_vars_right[index][1].config(text=text)
        elif side == "left_top":
            self.top_update_cb.config(text=text)
        elif side == "left_bottom":
            self.bottom_update_cb.config(text=text)

class HandleSystemController:
    
    def __init__(self, gui, station):
        self.station = station
        self.gui = gui
        mainThread = threading.Thread(
            target=asyncio.run, args=(self.mainTask(),), daemon=True
        )
        mainThread.start()
    
    async def mainTask(self):

        stat = 1
        self.gui.showStation(7)
        while True:

            await self.scanTask()
            print("BLScan")

            if stat == 1:
                if self.newScanDataAvail:
                    self.updateIcons()
                    self.newScanDataAvail = False
                else:
                    continue
                if self.gui.activeNode < 8:
                    nodeType = self.station.nodeStatus[self.gui.activeNode][3]
                    if nodeType == 0x0A:
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()

                else:
                    self.gui.clearLiveStation()
                    if self.gui.getAutoRestartStatus() == 1:
                        print("Auto Restart Sent")
                        self.stationReset = True
                        time.sleep(1)

            else:
                if self.gui.activeNode < 8:
                    nodeType = self.station.nodeStatus[self.gui.activeNode][3]
                    if nodeType == 0x0A:
                        self.gui.showLiveStation()
                    else:
                        self.gui.clearLiveStation()

                data = await self.scanDiags()
                # print(chr(27) + "[2J")
                # print("Node:  0  1  2  3  4  5  6  7")
                # print("     ", end=" ")
                # try:
                #     for i in range(3, 11):
                #         print(f"{data[i]:2d}", end=" ")
                # except:
                #     print("Data error")
                # print("curButton, NdType=", self.gui.activeNode, nodeType)
                # print(" ")
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = ControlWindow(root)
    station = Station(app)
    root.mainloop()
