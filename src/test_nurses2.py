
import asyncio
import wcwidth
import termios
import tty
import numpy
import cv2

try:
    import termios
    termios.set_raw_mode()
except:
    pass

import nurses_2

from nurses_2.app import App
from nurses_2.widgets.button import Button
from nurses_2.widgets.menu import Menu
from nurses_2.widgets.text_widget import TextWidget

from nurses_2.widgets.grid_layout import GridLayout, Orientation
from nurses_2.widgets.toggle_button import ToggleButton, ToggleState


from nurses_2.colors import DEFAULT_COLOR_THEME
from nurses_2.widgets.textbox import Textbox
from nurses_2.widgets.text_pad import TextPad
from nurses_2.widgets.text_widget import TextWidget
from nurses_2.widgets.widget import Widget



class MyApp(App):
    async def on_start(self):
        label = TextWidget(size=(1, 50))



        #=============================================================================

        display = TextWidget(size=(1, 20), pos=(6, 6))

        def button_callback(i):
            def callback():
                display.add_str(f"Button {i + 1} pressed!".ljust(20))
            return callback

        def toggle_button_callback(i):
            def callback(state):
                display.add_str(f"Button {i + 1} {'un' if state is ToggleState.OFF else ''}toggled!".ljust(20))
            return callback

        grid_layout = GridLayout(
            grid_rows=5,
            grid_columns=3,
            pos=(7, 7),
            orientation=Orientation.TB_LR,
            padding_top=1,
            padding_bottom=1,
            padding_left=1,
            padding_right=1,
            horizontal_spacing=1,
        )

        # Buttons
        grid_layout.add_widgets(
            Button(size=(1, 10), label=f"Button {i + 1}", callback=button_callback(i))
            for i in range(5)
        )

        # Independent toggle buttons
        grid_layout.add_widgets(
            ToggleButton(size=(1, 12), label=f"Button {i + 1}", callback=toggle_button_callback(i))
            for i in range(5, 10)
        )

        # Grouped radio buttons
        grid_layout.add_widgets(
            ToggleButton(
                size=(1, 12),
                group="my_group",
                label=f"Button {i + 1}",
                callback=toggle_button_callback(i),
            )
            for i in range(10, 15)
        )

        grid_layout.size = grid_layout.minimum_grid_size

        self.add_widgets(display, grid_layout)

        #=============================================================================


        def add_text(text):
            def inner():
                label.add_str(f"{text:<50}"[:50], truncate_str=True)
            return inner

        def add_text_toggle(text):
            def inner(toggle_state):
                label.add_str(f"{f'{text} {toggle_state}':<50}"[:50], truncate_str=True)
            return inner

        # These "keybinds" aren't implemented.
        menu_dict = {
            ("New File", "Ctrl+N"): add_text("New File"),
            ("Open File...", "Ctrl+O"): add_text("Open File..."),
            ("Save", "Ctrl+S"): add_text("Save"),
            ("Save as...", "Ctrl+Shift+S"): add_text("Save as..."),
            ("Preferences", ""): {
                ("Settings", "Ctrl+,"): add_text("Settings"),
                ("Keyboard Shortcuts", "Ctrl+K Ctrl+S"): add_text("Keyboard Shortcuts"),
                ("Toggle Item 1", ""): add_text_toggle("Toggle Item 1"),
                ("Toggle Item 2", ""): add_text_toggle("Toggle Item 2"),
            },
        }

        self.add_widget(label)
        self.add_widgets(Menu.from_dict_of_dicts(menu_dict, pos=(2, 0)))

        root_menu = self.children[-1]
        root_menu.is_enabled = False
        root_menu.children[1].item_disabled = True

        def toggle_root_menu():
            if root_menu.is_enabled:
                root_menu.close_menu()
            else:
                root_menu.open_menu()

        self.add_widget(Button(label="File", callback=toggle_root_menu, pos=(1, 0), size=(1, 6)))


        def enter_callback(textbox):
            textbox.text = ""

        # Note that `enter_callback` expects a callable with the textbox as the only argument.
        textbox = Textbox(pos=(1, 1), size=(1, 31), enter_callback=enter_callback, max_chars=50)

        color_pair = DEFAULT_COLOR_THEME.primary

        border = TextWidget(pos=(1, 0), size=(3, 33), default_color_pair=color_pair)
        border.add_border()
        border.add_widget(textbox)

        label = TextWidget(pos_hint=(None, .5), anchor="top_center", size=(1, 7), default_color_pair=color_pair)
        label.add_str("Textbox")

        container = Widget(
            size=(4, 33),
            pos_hint=(None, .5),
            anchor="top_center",
            background_color_pair=textbox.background_color_pair,
        )
        container.add_widgets(label, border)

        self.add_widget(container)

async def main():
    await MyApp(title="Menu Example")._run_async()


asyncio.run( main() )

