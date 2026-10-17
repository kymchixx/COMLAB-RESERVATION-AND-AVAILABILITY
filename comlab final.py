import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
BG = "#050817"
PANEL = "#0d1528"
PANEL_DARK = "#070d1d"
BORDER = "#202d45"
TEXT = "#e8f0ff"
MUTED = "#91a4c0"
CYAN = "#10c8e8"
BLUE = "#4d54f5"
GREEN = "#10c997"
RED = "#f43f67"
AMBER = "#f6a000"
PURPLE = "#a12df1"

LABS = [
    {
        "name": "ComLab 1: Information Technology",
        "subtitle": "Support Specialist",
        "icon": "</>",
        "accent": CYAN,
    },
    {
        "name": "ComLab 2: Computer Science",
        "subtitle": "Program and Software Development",
        "icon": "◈",
        "accent": BLUE,
    },
    {
        "name": "ComLab 3: Computer Engineering",
        "subtitle": "Design Computer Hardware",
        "icon": "✿",
        "accent": PURPLE,
    },
]


class ComLabReserve(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Computer Laboratory Reservation Availability System")
        self.geometry("1250x820")
        self.minsize(1000, 680)
        self.configure(bg=BG)

        self.selected_lab = 2
        self.role = tk.StringVar(value="Student")
        self.search_var = tk.StringVar()
        self.active_tab = tk.StringVar(
            value="Interactive 30-PC Floor Plan"
        )

        self.reservations = []
        self.pc_states = {}

        self._build_styles()
        self._seed_pc_states()
        self._build_header()
        self._build_main()
        self._render_all()
        self._tick_clock()

    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "TCombobox",
            fieldbackground=PANEL,
            background=PANEL,
            foreground=TEXT,
            arrowcolor=CYAN,
            bordercolor=BORDER,
        )

        style.map(
            "TCombobox",
            fieldbackground=[("readonly", PANEL)],
            foreground=[("readonly", TEXT)],
        )

        style.configure(
            "TEntry",
            fieldbackground=PANEL_DARK,
            foreground=TEXT,
            insertcolor=TEXT,
            bordercolor=BORDER,
            padding=8,
        )

        style.configure(
            "TScrollbar",
            background=PANEL,
            troughcolor=BG,
            bordercolor=BG,
            arrowcolor=MUTED,
        )

    def _seed_pc_states(self):
        for lab_index in range(3):
            self.pc_states[lab_index] = {
                f"PC-{n:02d}": "Available"
                for n in range(1, 31)
            }

        self.pc_states[2]["PC-03"] = "Occupied"
        self.pc_states[2]["PC-08"] = "Occupied"
        self.pc_states[2]["PC-17"] = "Maintenance"

        for lab_index in range(3):
            self.pc_states[lab_index]["PC-03"] = "Occupied"
            self.pc_states[lab_index]["PC-08"] = "Occupied"

    def _label(
        self,
        parent,
        text,
        size=10,
        color=TEXT,
        bold=False,
        **kwargs
    ):
        return tk.Label(
            parent,
            text=text,
            bg=kwargs.pop("bg", parent.cget("bg")),
            fg=color,
            font=(
                "Segoe UI",
                size,
                "bold" if bold else "normal"
            ),
            **kwargs,
        )

    def _button(
        self,
        parent,
        text,
        command,
        bg=PANEL,
        fg=TEXT,
        active=None,
        padx=12,
        pady=8,
        font_size=10,
        bold=False,
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=active or bg,
            activeforeground=TEXT,
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=padx,
            pady=pady,
            font=(
                "Segoe UI",
                font_size,
                "bold" if bold else "normal"
            ),
        )

    def _build_header(self):
        header = tk.Frame(
            self,
            bg="#10192b",
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=18,
            pady=12,
        )
        header.pack(fill="x")
        header.grid_columnconfigure(1, weight=1)

        brand = tk.Frame(header, bg="#10192b")
        brand.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 18),
        )

        self._label(
            brand,
            "▣  ComLab Reserve ³",
            18,
            CYAN,
            True,
        ).pack(anchor="w")

        self._label(
            brand,
            "Labs  ·  90 PCs",
            10,
            CYAN,
            True,
        ).pack(anchor="w", pady=(2, 0))

        self._label(
            brand,
            "Computer Laboratory Reservation &",
            9,
            MUTED,
        ).pack(anchor="w")

        self._label(
            brand,
            "Real-time Availability System",
            9,
            MUTED,
        ).pack(anchor="w")

        self.clock_label = self._label(
            header,
            "",
            10,
            TEXT,
            bg=PANEL_DARK,
            padx=14,
            pady=12,
            justify="left",
        )
        self.clock_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=8,
        )

        search_wrap = tk.Frame(
            header,
            bg=PANEL_DARK,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        search_wrap.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=8,
        )

        self._label(
            search_wrap,
            "⌕",
            16,
            MUTED,
            bg=PANEL_DARK,
        ).pack(side="left", padx=(10, 4))

        entry = ttk.Entry(
            search_wrap,
            textvariable=self.search_var,
            width=24,
        )
        entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6,
            padx=(0, 8),
        )

        entry.bind(
            "<KeyRelease>",
            lambda _event: self._render_floorplan(),
        )

        role_frame = tk.Frame(
            header,
            bg=PANEL_DARK,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=4,
            pady=4,
        )
        role_frame.grid(row=0, column=3, padx=8)

        for role in ("Student", "Instructor", "Lab Admin"):
            self._button(
                role_frame,
                role,
                lambda selected_role=role: self._set_role(
                    selected_role
                ),
                bg=(
                    CYAN
                    if role == self.role.get()
                    else PANEL_DARK
                ),
                fg=(
                    "#03101c"
                    if role == self.role.get()
                    else MUTED
                ),
                padx=9,
                pady=9,
                font_size=9,
                bold=True,
            ).pack(side="left")

        self._button(
            header,
            "+  Book\nReservation",
            self._open_booking,
            bg="#167fd2",
            active=BLUE,
            fg="white",
            padx=15,
            pady=10,
            font_size=10,
            bold=True,
        ).grid(
            row=0,
            column=4,
            padx=(8, 0),
        )

    def _build_main(self):
        outer = tk.Frame(self, bg=BG)
        outer.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            outer,
            bg=BG,
            highlightthickness=0,
        )

        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.content = tk.Frame(
            self.canvas,
            bg=BG,
            padx=22,
            pady=18,
        )

        self.content_window = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.content.bind(
            "<Configure>",
            lambda _event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            ),
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.content_window,
                width=event.width,
            ),
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self._mousewheel,
        )

        self.stats_frame = tk.Frame(
            self.content,
            bg=BG,
        )
        self.stats_frame.pack(
            fill="x",
            pady=(0, 22),
        )

        self.lab_frame = tk.Frame(
            self.content,
            bg=BG,
        )
        self.lab_frame.pack(
            fill="x",
            pady=(0, 20),
        )

        self.tabs_frame = tk.Frame(
            self.content,
            bg=BG,
        )
        self.tabs_frame.pack(
            fill="x",
            pady=(0, 14),
        )

        self.panel = tk.Frame(
            self.content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=20,
            pady=18,
        )
        self.panel.pack(
            fill="both",
            expand=True,
        )

    def _mousewheel(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units",
        )

    def _set_role(self, role):
        self.role.set(role)
        self._render_all()

    def _render_all(self):
        for frame in (
            self.stats_frame,
            self.lab_frame,
            self.tabs_frame,
            self.panel,
        ):
            for child in frame.winfo_children():
                child.destroy()

        self._render_stats()
        self._render_labs()
        self._render_tabs()
        self._render_panel()

    def _render_stats(self):
        states = self.pc_states[self.selected_lab]

        available = sum(
            value == "Available"
            for value in states.values()
        )
        occupied = sum(
            value == "Occupied"
            for value in states.values()
        )
        maintenance = sum(
            value == "Maintenance"
            for value in states.values()
        )

        cards = [
            (
                "Total Workstations",
                "30",
                "Across 3 computer labs",
                CYAN,
            ),
            (
                "Available PCs",
                str(available),
                "Ready for reservation",
                GREEN,
            ),
            (
                "Currently Occupied",
                str(occupied),
                "In use right now",
                RED,
            ),
            (
                "Maintenance",
                str(maintenance),
                "Temporarily unavailable",
                AMBER,
            ),
            (
                "Occupancy Rate",
                f"{round(occupied / 30 * 100)}%",
                "Live Telemetry",
                BLUE,
            ),
        ]

        for i, (title, value, subtitle, accent) in enumerate(cards):
            card = tk.Frame(
                self.stats_frame,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1,
                padx=16,
                pady=14,
            )

            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 10, 0),
            )

            self.stats_frame.grid_columnconfigure(
                i,
                weight=1,
                uniform="stats",
            )

            self._label(
                card,
                title,
                10,
                MUTED,
                bg=PANEL,
            ).pack(anchor="w")

            row = tk.Frame(card, bg=PANEL)
            row.pack(fill="x", pady=(10, 2))

            self._label(
                row,
                value,
                22,
                accent,
                True,
                bg=PANEL,
            ).pack(side="left")

            self._label(
                row,
                "●",
                10,
                accent,
                bg=PANEL,
            ).pack(side="right", padx=4)

            self._label(
                card,
                subtitle,
                8,
                MUTED,
                bg=PANEL,
            ).pack(anchor="w")

    def _render_labs(self):
        for i, lab in enumerate(LABS):
            states = self.pc_states[i]

            available = sum(
                value == "Available"
                for value in states.values()
            )

            card = tk.Frame(
                self.lab_frame,
                bg=PANEL,
                highlightbackground=(
                    CYAN if i == self.selected_lab else BORDER
                ),
                highlightthickness=1,
                padx=14,
                pady=13,
                cursor="hand2",
            )

            card.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=(0 if i == 0 else 12, 0),
            )

            self.lab_frame.grid_columnconfigure(
                i,
                weight=1,
                uniform="labs",
            )

            card.bind(
                "<Button-1>",
                lambda _event, index=i: self._select_lab(index),
            )

            icon = self._label(
                card,
                lab["icon"],
                17,
                "white",
                True,
                bg=lab["accent"],
                padx=10,
                pady=8,
            )
            icon.grid(
                row=0,
                column=0,
                rowspan=2,
                sticky="w",
                padx=(0, 12),
            )

            title = self._label(
                card,
                lab["name"],
                10,
                TEXT,
                True,
                bg=PANEL,
                wraplength=205,
                justify="left",
            )
            title.grid(
                row=0,
                column=1,
                sticky="w",
            )

            subtitle = self._label(
                card,
                lab["subtitle"],
                8,
                MUTED,
                bg=PANEL,
                wraplength=215,
                justify="left",
            )
            subtitle.grid(
                row=1,
                column=1,
                sticky="w",
                pady=(4, 0),
            )

            self._label(
                card,
                f"{available}/30",
                12,
                GREEN,
                True,
                bg=PANEL,
            ).grid(
                row=0,
                column=2,
                padx=(8, 0),
                sticky="e",
            )

            self._label(
                card,
                "AVAILABLE",
                8,
                MUTED,
                bg=PANEL,
            ).grid(
                row=1,
                column=2,
                padx=(8, 0),
                sticky="e",
            )

            for widget in card.winfo_children():
                widget.bind(
                    "<Button-1>",
                    lambda _event, index=i: self._select_lab(index),
                )

    def _select_lab(self, index):
        self.selected_lab = index
        self._render_all()

    def _render_tabs(self):
        tabs = [
            (
                "▦  Interactive 30-PC Floor Plan",
                "Interactive 30-PC Floor Plan",
            ),
            (
                "▦  Lab Timetable Grid",
                "Lab Timetable Grid",
            ),
            (
                f"▣  My Passes / Management  {len(self.reservations)}",
                "My Passes / Management",
            ),
            (
                "⌁  Analytics & Hardware Demand",
                "Analytics & Hardware Demand",
            ),
        ]

        for label, key in tabs:
            active = self.active_tab.get() == key

            self._button(
                self.tabs_frame,
                label,
                lambda selected_tab=key: self._set_tab(
                    selected_tab
                ),
                bg="#073044" if active else BG,
                fg=CYAN if active else MUTED,
                active="#073044",
                padx=13,
                pady=11,
                font_size=9,
                bold=active,
            ).pack(
                side="left",
                padx=(0, 8),
            )

        tk.Frame(
            self.tabs_frame,
            bg=BORDER,
            height=1,
        ).pack(
            fill="x",
            side="bottom",
            pady=(12, 0),
        )

    def _set_tab(self, tab):
        self.active_tab.set(tab)
        self._render_all()

    def _render_panel(self):
        tab = self.active_tab.get()

        if tab == "Interactive 30-PC Floor Plan":
            self._render_floorplan()
        elif tab == "Lab Timetable Grid":
            self._render_timetable()
        elif tab == "My Passes / Management":
            self._render_reservations()
        else:
            self._render_analytics()

    def _render_floorplan(self):
        if self.active_tab.get() != "Interactive 30-PC Floor Plan":
            return

        for child in self.panel.winfo_children():
            child.destroy()

        legend = tk.Frame(
            self.panel,
            bg=PANEL_DARK,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=14,
            pady=10,
        )
        legend.pack(
            fill="x",
            pady=(0, 20),
        )

        self._label(
            legend,
            "Seat Legend:",
            9,
            MUTED,
            bg=PANEL_DARK,
        ).pack(
            side="left",
            padx=(0, 22),
        )

        for status, color in (
            ("Available", GREEN),
            ("Occupied", RED),
            ("Maintenance", AMBER),
        ):
            self._label(
                legend,
                f"●  {status}",
                9,
                color,
                bg=PANEL_DARK,
            ).pack(
                side="left",
                padx=(0, 20),
            )

        self._label(
            legend,
            f"Showing 30 PC Stations for {LABS[self.selected_lab]['name']}",
            8,
            CYAN,
            True,
            bg=PANEL_DARK,
        ).pack(side="right")

        room = tk.Frame(
            self.panel,
            bg="#0a1224",
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=18,
            pady=18,
        )
        room.pack(
            fill="x",
        )

        front = tk.Frame(
            room,
            bg=PANEL_DARK,
            highlightbackground=BORDER,
            highlightthickness=1,
            pady=15,
        )
        front.pack(
            fill="x",
            pady=(0, 22),
        )

        self._label(
            front,
            "▣   INSTRUCTOR PODIUM & SMART PROJECTOR SCREEN (FRONT)",
            10,
            CYAN,
            bg=PANEL_DARK,
        ).pack()

        states = self.pc_states[self.selected_lab]
        query = self.search_var.get().strip().lower()

        for row_start in range(0, 30, 5):
            row = tk.Frame(
                room,
                bg="#0a1224",
            )
            row.pack(
                fill="x",
                pady=(0, 14),
            )

            for n in range(
                row_start + 1,
                min(row_start + 6, 31),
            ):
                pc = f"PC-{n:02d}"
                status = states[pc]

                if (
                    query
                    and query not in pc.lower()
                    and query not in status.lower()
                ):
                    card = tk.Frame(
                        row,
                        bg="#0a1224",
                        width=150,
                        height=132,
                    )
                    card.pack(
                        side="left",
                        fill="both",
                        expand=True,
                        padx=7,
                    )
                    card.pack_propagate(False)
                    continue

                if status == "Available":
                    color = GREEN
                    card_bg = "#0b1928"
                    outline = "#075f55"
                elif status == "Occupied":
                    color = RED
                    card_bg = "#171326"
                    outline = "#7c2442"
                else:
                    color = AMBER
                    card_bg = "#211a0b"
                    outline = "#78510a"

                card = tk.Frame(
                    row,
                    bg=card_bg,
                    highlightbackground=outline,
                    highlightthickness=1,
                    padx=12,
                    pady=10,
                    cursor="hand2",
                )

                card.pack(
                    side="left",
                    fill="both",
                    expand=True,
                    padx=7,
                )

                top = tk.Frame(
                    card,
                    bg=card_bg,
                )
                top.pack(fill="x")

                self._label(
                    top,
                    pc,
                    9,
                    TEXT,
                    True,
                    bg=card_bg,
                ).pack(side="left")

                self._label(
                    top,
                    "●",
                    11,
                    color,
                    bg=card_bg,
                ).pack(side="right")

                self._label(
                    card,
                    "▰",
                    26,
                    color,
                    True,
                    bg=card_bg,
                ).pack(pady=(7, 1))

                self._label(
                    card,
                    "NVIDIA RTX 4080",
                    8,
                    TEXT,
                    bg=card_bg,
                ).pack()

                tk.Frame(
                    card,
                    bg=BORDER,
                    height=1,
                ).pack(
                    fill="x",
                    pady=7,
                )

                bottom = tk.Frame(
                    card,
                    bg=card_bg,
                )
                bottom.pack(fill="x")

                self._label(
                    bottom,
                    "64GB DDR5",
                    7,
                    MUTED,
                    bg=card_bg,
                ).pack(side="left")

                self._label(
                    bottom,
                    status.upper(),
                    7,
                    color,
                    bg=card_bg,
                ).pack(side="right")

                card.bind(
                    "<Button-1>",
                    lambda _event, selected_pc=pc: self._select_pc(
                        selected_pc
                    ),
                )

                for widget in card.winfo_children():
                    widget.bind(
                        "<Button-1>",
                        lambda _event, selected_pc=pc: self._select_pc(
                            selected_pc
                        ),
                    )

        self._label(
            self.panel,
            "Tip: Select an available PC to reserve it. "
            "Occupied and maintenance PCs cannot be booked.",
            9,
            MUTED,
        ).pack(
            anchor="w",
            pady=(14, 0),
        )

    def _select_pc(self, pc):
        status = self.pc_states[self.selected_lab][pc]

        if status != "Available":
            messagebox.showinfo(
                "PC unavailable",
                f"{pc} is currently {status.lower()}.",
            )
            return

        self._open_booking(pc)

    def _open_booking(self, pc=None):
        win = tk.Toplevel(self)
        win.title("Book Reservation")
        win.configure(bg=BG)
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()

        frame = tk.Frame(
            win,
            bg=PANEL,
            padx=22,
            pady=20,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12,
        )

        self._label(
            frame,
            "Book a Computer Reservation",
            15,
            CYAN,
            True,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(0, 16),
        )

        fields = tk.Frame(
            frame,
            bg=PANEL,
        )
        fields.pack(fill="x")

        lab_var = tk.StringVar(
            value=LABS[self.selected_lab]["name"]
        )

        available_pcs = [
            station
            for station, state in self.pc_states[
                self.selected_lab
            ].items()
            if state == "Available"
        ]

        pc_var = tk.StringVar(
            value=(
                pc
                or (available_pcs[0] if available_pcs else "")
            )
        )

        user_var = tk.StringVar()
        date_var = tk.StringVar(
            value=datetime.now().strftime("%Y-%m-%d")
        )
        start_var = tk.StringVar(value="09:00")
        duration_var = tk.StringVar(value="1 hour")

        field_specs = [
            (
                "Laboratory",
                lab_var,
                [lab["name"] for lab in LABS],
            ),
            (
                "PC Station",
                pc_var,
                list(self.pc_states[self.selected_lab].keys()),
            ),
            (
                "Student / Instructor Name",
                user_var,
                None,
            ),
            (
                "Date (YYYY-MM-DD)",
                date_var,
                None,
            ),
            (
                "Start Time (HH:MM)",
                start_var,
                None,
            ),
            (
                "Duration",
                duration_var,
                ["1 hour", "2 hours", "3 hours"],
            ),
        ]

        for label, variable, values in field_specs:
            self._label(
                fields,
                label,
                9,
                MUTED,
                bg=PANEL,
            ).pack(
                anchor="w",
                pady=(5, 3),
            )

            if values:
                widget = ttk.Combobox(
                    fields,
                    textvariable=variable,
                    values=values,
                    state="readonly",
                    width=38,
                )
                widget.pack(
                    fill="x",
                    ipady=3,
                )

                if label == "Laboratory":
                    widget.bind(
                        "<<ComboboxSelected>>",
                        lambda _event: self._update_booking_pcs(
                            lab_var,
                            pc_var,
                        ),
                    )
            else:
                ttk.Entry(
                    fields,
                    textvariable=variable,
                    width=40,
                ).pack(
                    fill="x",
                    ipady=3,
                )

        def submit():
            lab_index = next(
                i
                for i, item in enumerate(LABS)
                if item["name"] == lab_var.get()
            )

            chosen_pc = pc_var.get()

            if not user_var.get().strip():
                messagebox.showwarning(
                    "Missing name",
                    "Please enter your name.",
                    parent=win,
                )
                return

            if chosen_pc not in self.pc_states[lab_index]:
                messagebox.showwarning(
                    "Choose a PC",
                    "Please select a PC station.",
                    parent=win,
                )
                return

            if self.pc_states[lab_index][chosen_pc] != "Available":
                messagebox.showwarning(
                    "PC unavailable",
                    f"{chosen_pc} is not available.",
                    parent=win,
                )
                return

            try:
                datetime.strptime(
                    date_var.get(),
                    "%Y-%m-%d",
                )
                datetime.strptime(
                    start_var.get(),
                    "%H:%M",
                )
            except ValueError:
                messagebox.showwarning(
                    "Invalid date or time",
                    "Use YYYY-MM-DD and 24-hour HH:MM format.",
                    parent=win,
                )
                return

            record = {
                "lab": lab_var.get(),
                "pc": chosen_pc,
                "name": user_var.get().strip(),
                "date": date_var.get(),
                "start": start_var.get(),
                "duration": duration_var.get(),
                "role": self.role.get(),
                "pass": f"CL-{random.randint(10000, 99999)}",
            }

            self.reservations.append(record)
            self.pc_states[lab_index][chosen_pc] = "Occupied"
            self.selected_lab = lab_index

            win.destroy()
            self._render_all()

            messagebox.showinfo(
                "Reservation confirmed",
                f"Reservation saved!\n\n"
                f"Pass: {record['pass']}\n"
                f"{record['lab']}\n"
                f"{record['pc']} · {record['date']} "
                f"at {record['start']}",
            )

        self._button(
            frame,
            "Confirm Reservation",
            submit,
            bg=CYAN,
            fg="#03101c",
            active=BLUE,
            padx=14,
            pady=11,
            bold=True,
        ).pack(
            fill="x",
            pady=(18, 0),
        )

        self._button(
            frame,
            "Cancel",
            win.destroy,
            bg=PANEL_DARK,
            fg=MUTED,
            padx=14,
            pady=8,
        ).pack(
            fill="x",
            pady=(7, 0),
        )

    def _update_booking_pcs(self, lab_var, pc_var):
        index = next(
            i
            for i, lab in enumerate(LABS)
            if lab["name"] == lab_var.get()
        )

        available = [
            pc
            for pc, state in self.pc_states[index].items()
            if state == "Available"
        ]

        pc_var.set(available[0] if available else "")

    def _render_timetable(self):
        self._label(
            self.panel,
            "Laboratory Timetable Grid",
            15,
            CYAN,
            True,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(0, 8),
        )

        self._label(
            self.panel,
            "Sample weekly schedule · select Book Reservation "
            "to create a new booking.",
            9,
            MUTED,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(0, 18),
        )

        days = [
            "Time",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
        ]

        table = tk.Frame(
            self.panel,
            bg=BORDER,
            padx=1,
            pady=1,
        )
        table.pack(fill="x")

        for column, day in enumerate(days):
            self._label(
                table,
                day,
                9,
                CYAN if column else MUTED,
                True,
                bg=PANEL_DARK,
                padx=9,
                pady=10,
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            table.grid_columnconfigure(
                column,
                weight=1,
            )

        times = [
            "08:00–10:00",
            "10:00–12:00",
            "12:00–14:00",
            "14:00–16:00",
            "16:00–18:00",
        ]

        for row_number, time in enumerate(times, 1):
            self._label(
                table,
                time,
                8,
                MUTED,
                bg=PANEL,
                padx=7,
                pady=12,
            ).grid(
                row=row_number,
                column=0,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            for column in range(1, 6):
                reserved = (
                    row_number + column + self.selected_lab
                ) % 4 == 0

                status = "Reserved" if reserved else "Available"
                color = RED if reserved else GREEN

                self._label(
                    table,
                    status,
                    8,
                    color,
                    bg="#10172a",
                    padx=7,
                    pady=12,
                ).grid(
                    row=row_number,
                    column=column,
                    sticky="nsew",
                    padx=1,
                    pady=1,
                )

    def _render_reservations(self):
        self._label(
            self.panel,
            "My Passes / Reservation Management",
            15,
            CYAN,
            True,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(0, 14),
        )

        if not self.reservations:
            self._label(
                self.panel,
                "No reservations yet. Click “Book Reservation” "
                "to create your first pass.",
                10,
                MUTED,
                bg=PANEL,
            ).pack(
                anchor="w",
                pady=15,
            )
            return

        headers = [
            "Pass ID",
            "Name",
            "Laboratory",
            "PC",
            "Date",
            "Start",
            "Duration",
            "Role",
        ]

        table = tk.Frame(
            self.panel,
            bg=BORDER,
            padx=1,
            pady=1,
        )
        table.pack(fill="x")

        for column, heading in enumerate(headers):
            self._label(
                table,
                heading,
                8,
                CYAN,
                True,
                bg=PANEL_DARK,
                padx=6,
                pady=9,
            ).grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            table.grid_columnconfigure(
                column,
                weight=1,
            )

        for row_number, record in enumerate(
            self.reservations,
            1,
        ):
            values = [
                record["pass"],
                record["name"],
                record["lab"],
                record["pc"],
                record["date"],
                record["start"],
                record["duration"],
                record["role"],
            ]

            for column, value in enumerate(values):
                self._label(
                    table,
                    value,
                    8,
                    TEXT,
                    bg=PANEL,
                    padx=5,
                    pady=10,
                    wraplength=130,
                ).grid(
                    row=row_number,
                    column=column,
                    sticky="nsew",
                    padx=1,
                    pady=1,
                )

        self._button(
            self.panel,
            "Cancel Latest Reservation",
            self._cancel_latest,
            bg="#4a1930",
            fg="#ff8da5",
            padx=12,
            pady=9,
        ).pack(
            anchor="w",
            pady=(14, 0),
        )

    def _cancel_latest(self):
        if not self.reservations:
            return

        record = self.reservations.pop()

        lab_index = next(
            i
            for i, lab in enumerate(LABS)
            if lab["name"] == record["lab"]
        )

        self.pc_states[lab_index][record["pc"]] = "Available"
        self._render_all()

    def _render_analytics(self):
        self._label(
            self.panel,
            "Analytics & Hardware Demand",
            15,
            CYAN,
            True,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(0, 15),
        )

        for index, lab in enumerate(LABS):
            states = self.pc_states[index]

            available = sum(
                state == "Available"
                for state in states.values()
            )

            occupied = sum(
                state == "Occupied"
                for state in states.values()
            )

            maintenance = sum(
                state == "Maintenance"
                for state in states.values()
            )

            row = tk.Frame(
                self.panel,
                bg=PANEL_DARK,
                padx=12,
                pady=12,
                highlightbackground=BORDER,
                highlightthickness=1,
            )
            row.pack(
                fill="x",
                pady=6,
            )

            self._label(
                row,
                lab["name"],
                10,
                TEXT,
                True,
                bg=PANEL_DARK,
            ).pack(anchor="w")

            self._label(
                row,
                f"Available: {available}    "
                f"Occupied: {occupied}    "
                f"Maintenance: {maintenance}",
                9,
                GREEN,
                bg=PANEL_DARK,
            ).pack(
                anchor="w",
                pady=(6, 0),
            )

            bar = tk.Canvas(
                row,
                height=10,
                bg="#1d2940",
                highlightthickness=0,
            )
            bar.pack(
                fill="x",
                pady=(10, 0),
            )

            bar.update_idletasks()
            width = max(bar.winfo_width(), 300)

            bar.create_rectangle(
                0,
                0,
                width * available / 30,
                10,
                fill=GREEN,
                outline="",
            )

            bar.create_rectangle(
                width * available / 30,
                0,
                width * (available + occupied) / 30,
                10,
                fill=RED,
                outline="",
            )

            bar.create_rectangle(
                width * (available + occupied) / 30,
                0,
                width,
                10,
                fill=AMBER,
                outline="",
            )

        self._label(
            self.panel,
            "Hardware profile: NVIDIA RTX 4080 · "
            "64GB DDR5 · 30 stations per laboratory",
            9,
            MUTED,
            bg=PANEL,
        ).pack(
            anchor="w",
            pady=(14, 0),
        )

    def _tick_clock(self):
        now = datetime.now()

        self.clock_label.configure(
            text=(
                f"◷  {now.strftime('%a, %b %d')}\n"
                f"    {now.strftime('%I:%M %p')}"
            )
        )

        self.after(
            30000,
            self._tick_clock,
        )


if __name__ == "__main__":
    app = ComLabReserve()
    app.mainloop()