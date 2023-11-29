#!python3

# /// pyproject
# [project]
# name = "name"
# version = "version"
# description = "description"
# readme = {file = "README.txt", content-type = "text/markdown"}
# requires-python = ">=3.11"
#
# dependencies = [
#    "importlib_metadata",
#    "pygments",
#    "typing-extensions",
#    "markdown-it-py",
#    "mdurl",
#    "zipp",
#    "linkify-it-py",
#    "mdit-py-plugins",
#    "uc-micro-py",
#    "rich",
#    "pyperclip",
#    "textual",
# ]
# ///



import asyncio, threading
import re
import shutil
import time

import os
os.environ["FORCE_COLOR"] = "1"

from functools import partial
from pathlib import Path


import textual

SCM_PATH = Path(textual.__file__).parent / "tree-sitter/highlights"

from textual.app import App, ComposeResult
from textual.widgets import (
    Markdown,
    TextArea,
    Markdown,
    DirectoryTree,
    Markdown,
    Label,
    Input,
    Switch,
    Button,
    Footer,
    MarkdownViewer,
    Tree,
)
from textual.widgets.text_area import LanguageDoesNotExist
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.screen import ModalScreen
from textual.validation import Length
from textual.events import Event
from textual import work
from textual.binding import Binding
from textual import events
from textual.command import Hit, Hits, Provider
from textual._slug import TrackedSlugs

with open("noteri.tcss","w") as file:
    file.write("""
DirectoryTree {
    width: auto;
    scrollbar-size: 1 1;
    dock: left;
}

#md {
    width: 100%;
}

#title {
    width: 100%;
    align: center middle;
}

ScrollableContainer {
    scrollbar-gutter: auto;
    scrollbar-size: 1 1;
}

#scrollable_markdown {
    width: 100%
}

#markdown {
    height: auto;
}
#backlinks {
    width: 100%;
}

TextArea {
    width: 100%;
    scrollbar-size: 1 1;
    scrollbar-size-vertical: 1;
}

#footer {
    dock: bottom;
}
""")


with open("README.md","w") as file:
    file.write("""# Noteri
A text editor built using textual.

## Install

Install xclip on linux for copy and paste functionality

```bash
sudo apt-get install xclip
```

```
pip install -r requirements
```

## Features

### Markdown Viewer

View markdown documents. Will search for backlinks in path. Prints title at top of documents.

### Command Pallet

`cmd + /` to open command pallet. Some commands have key bindings.

#### Application

`Toggle`: toggle on and off display of widgets


#### File Operations
- `New File`: Create a new file.
    - `ctrl+n`
- `New Directory`: Create a new directory.

- `Open`: open a file by name

- `Save`: Save the current editor
    - `ctrl+s`

- `Save As`: Input name to save file.

- `Rename`: Change the name of the file.

- `Delete`: Deletes file or directory.
   - `ctrl+d`


#### Text Editor
- `Copy`: Copy selection to clipboard.
    - TODO: Fix keybinding
- `Cut`: Cut from file into clipboard.
    - `ctrl+x`
- `Paste`: Paste from clipboard into file.
    - `ctrl+v`
- `Link [FILE PATH]`: Link another file

- `Table`: Create a table. With nothing selected, prompts user for row and column size. With selection, will format a table to look nice. Support for tab and return in table.

- `Bullet`: Make a bulleted list out of selection

- `Numbered List`: Make a numbered list out of selection.

- `Table of Contents`: Table of contents from Headings in markdown document.

- `Undo`: Undo text
    - `ctrl+z`
- `Redo`: Redo text
    - `ctrl+y`

## Example Images

![](example_image.png)
""")
try:
    import pyperclip
except:
    pyperclip = None

try:
    from tree_sitter_languages import get_language
except:
    get_language = None


# TODO: File Exists new file check
# TODO:


class WidgetCommands(Provider):
    async def startup(self) -> None:
        self.widgets = ["DirectoryTree", "#markdown", "TextArea", "#footer"]

    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, Noteri)

        for widget in self.widgets:
            command = f"Toggle {str(widget)}"
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),
                    partial(app.toggle_widget_display, widget),
                    help="Toggle this widget",
                )


class FileCommands(Provider):
    def _read_files_helper(self, path, depth=0):
        file_list = []
        if depth == 5:
            return []

        l = list(Path(path).glob("*"))

        for p in l:
            if p.name[0] == "." or p.name[0] == "venv":
                continue
            if p.is_dir():
                for item in self._read_files_helper(p, depth=depth + 1):
                    file_list.append(item)
            elif p.is_file():
                file_list.append(p)
        return file_list

    def read_files(self) -> list[Path]:
        return self._read_files_helper(Path(self.app.directory))
        # return list(Path(self.app.directory).glob("*.*"))

    async def startup(self) -> None:
        """Called once when the command palette is opened, prior to searching."""
        worker = self.app.run_worker(self.read_files, thread=True)
        self.file_paths = await worker.wait()

    async def search(self, query: str) -> Hits:
        """Search for files."""
        matcher = self.matcher(query)
        app = self.app
        assert isinstance(app, Noteri)

        commands = {
            "Open": app.open_file,
            "Link File": app.create_link,
        }

        # Open File
        for command, action in commands.items():
            for path in self.file_paths:
                full_command = f"{command} {str(path)}"
                score = matcher.match(full_command)

                # Open File
                if score > 0:
                    yield Hit(
                        score,
                        matcher.highlight(full_command),
                        partial(action, path),
                        # help="Open this file in the viewer",
                    )

        # Define a map of commands and their respective actions
        commands = {
            "New File": partial(app.action_new),
            "Save As": partial(app.action_save_as),
            "Save": partial(app.action_save),
            "Rename": partial(app.action_rename),
            "Delete": partial(app.action_delete),
            "Find": partial(app.action_find),
            "New Directory": partial(app.action_new_directory),
            "Cut": partial(app.action_cut),
            "Copy": partial(app.action_copy),
            "Paste": partial(app.action_paste),
            "Table": partial(app.action_table),
            "Bullet List": partial(app.action_bullet_list),
            "Numbered List": partial(app.action_numbered_list),
            "Code Block": partial(app.action_code_block),
            "Create Link": partial(app.action_create_link),
            "Copy Link": partial(app.action_copy_link),
            "Block Quote": partial(app.action_block_quote),
            "Bold": partial(app.action_bold),
            "Italic": partial(app.action_italic),
            "Strikethrough": partial(app.action_strikethrough),
            "Horizontal Rule": partial(app.action_horizontal_rule),
            "Table of Contents": partial(app.action_table_of_contents),
            "Directory Table of Contents": partial(app.action_directory_table_of_contents),
            "Heading 1": partial(app.action_heading, 1),
            "Heading 2": partial(app.action_heading, 2),
            "Heading 3": partial(app.action_heading, 3),
            "Heading 4": partial(app.action_heading, 4),
            "Heading 5": partial(app.action_heading, 5),
            "Heading 6": partial(app.action_heading, 6),
        }

        # Loop through the commands map
        for command, action in commands.items():
            score = matcher.match(command)
            if score > 0:
                yield Hit(score, matcher.highlight(command), action)


class MarkdownTablePopup(ModalScreen):
    BINDINGS = [("escape", "pop_screen")]

    def __init__(self, callback, validators=None):
        super().__init__()
        self.callback = callback
        self.validators = validators

    def compose(self) -> ComposeResult:
        yield Label("Header")
        yield Switch(id="header")
        yield Label("Rows")
        yield Input(validators=self.validators, id="rows")
        yield Label("Columns")
        yield Input(validators=self.validators, id="columns")

    @textual.on(Input.Submitted)
    def submitted(self, event: Input.Submitted):
        rows = int(self.query_one("#rows", expect_type=Input).value)
        columns = int(self.query_one("#columns", expect_type=Input).value)
        header = self.query_one("#header", expect_type=Switch).value
        self.app.post_message(Noteri.FileSystemCallback(self.callback, (rows, columns, header)))
        self.app.pop_screen()


class InputPopup(ModalScreen):
    BINDINGS = [("escape", "pop_screen")]

    def __init__(self, callback, title="Input", validators=None, default=""):
        super().__init__()
        self.callback = callback
        self.title = title
        self.validators = validators
        self.default = default

    def compose(self) -> ComposeResult:
        yield Label(self.title)
        yield Input(validators=self.validators, value=self.default)

    # def on_mount(self):
    #     self.query_one("Input", expect_type=Input).focus()

    @textual.on(Input.Submitted)
    def submitted(self, event: Input.Submitted):
        self.app.post_message(Noteri.FileSystemCallback(self.callback, (event.input.value,)))
        self.app.pop_screen()


class YesNoPopup(ModalScreen):
    BINDINGS = [("escape", "pop_screen")]

    def __init__(self, title, callback, message="") -> None:
        super().__init__()
        self.callback = callback
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        yield Label(self.title)
        yield Label(self.message)
        yield Button("Yes", id="yes")
        yield Button("No", id="no", variant="error")

    @textual.on(Button.Pressed, "#yes")
    def yes(self, event: Button.Pressed):
        self.app.post_message(Noteri.FileSystemCallback(self.callback, (True,)))
        self.app.pop_screen()

    @textual.on(Button.Pressed, "#no")
    def no(self, event: Button.Pressed):
        self.app.post_message(Noteri.FileSystemCallback(self.callback, (False,)))
        self.app.pop_screen()


class FileSelectionPopup(ModalScreen):
    BINDINGS = [("escape", "pop_screen")]

    def __init__(self, title, callback, message="") -> None:
        super().__init__()
        self.callback = callback
        self.title = title
        self.message = message

        self.selected_file = None

    def compose(self) -> ComposeResult:
        yield DirectoryTree()
        yield Label()
        yield Button("Create Link", "#create")

    @textual.on(DirectoryTree.FileSelected)
    def file_selected(self, message: DirectoryTree.FileSelected):
        self.selected_file = Path(message.path)

    @textual.on(Button.Pressed, "#Create")
    def yes(self, event: Button.Pressed):
        self.app.post_message(Noteri.FileSystemCallback(self.callback, self.selected_file))
        self.app.pop_screen()


class ExtendedTextArea(TextArea):
    """A subclass of TextArea with parenthesis-closing functionality."""

    BINDINGS = [
        Binding("escape", "screen.focus_next", "Shift Focus", show=False),
        # Cursor movement
        Binding("up", "cursor_up", "cursor up", show=False),
        Binding("down", "cursor_down", "cursor down", show=False),
        Binding("left", "cursor_left", "cursor left", show=False),
        Binding("right", "cursor_right", "cursor right", show=False),
        Binding("ctrl+left", "cursor_word_left", "cursor word left", show=False),
        Binding("ctrl+right", "cursor_word_right", "cursor word right", show=False),
        Binding("home,ctrl+a", "cursor_line_start", "cursor line start", show=False),
        Binding("end,ctrl+e", "cursor_line_end", "cursor line end", show=False),
        Binding("pageup", "cursor_page_up", "cursor page up", show=False),
        Binding("pagedown", "cursor_page_down", "cursor page down", show=False),
        # Making selections (generally holding the shift key and moving cursor)
        Binding(
            "ctrl+shift+left",
            "cursor_word_left(True)",
            "cursor left word select",
            show=False,
        ),
        Binding(
            "ctrl+shift+right",
            "cursor_word_right(True)",
            "cursor right word select",
            show=False,
        ),
        Binding(
            "shift+home",
            "cursor_line_start(True)",
            "cursor line start select",
            show=False,
        ),
        Binding("shift+end", "cursor_line_end(True)", "cursor line end select", show=False),
        Binding("shift+up", "cursor_up(True)", "cursor up select", show=False),
        Binding("shift+down", "cursor_down(True)", "cursor down select", show=False),
        Binding("shift+left", "cursor_left(True)", "cursor left select", show=False),
        Binding("shift+right", "cursor_right(True)", "cursor right select", show=False),
        # Shortcut ways of making selections
        # Binding("f5", "select_word", "select word", show=False),
        Binding("f6", "select_line", "select line", show=False),
        Binding("f7", "select_all", "select all", show=False),
        # Deletion
        Binding("backspace", "delete_left", "delete left", show=False),
        Binding("ctrl+w", "delete_word_left", "delete left to start of word", show=False),
        Binding("delete,ctrl+d", "delete_right", "delete right", show=False),
        Binding("ctrl+u", "delete_to_start_of_line", "delete to line start", show=False),
        Binding("ctrl+k", "delete_to_end_of_line", "delete to line end", show=False),
    ]

    def _insert_bookend_pair(self, bookend_start: str, bookend_end: str, only_selection=False) -> None:
        self.selected_text
        if self.selected_text == "" and not only_selection:
            # check if surrounding text is already a pair
            start = self.cursor_location
            start = (start[0], start[1] - 1)
            end = self.cursor_location
            end = (end[0], end[1] + 1)

            if self.get_text_range(start, end) == bookend_start + bookend_end:
                self.move_cursor_relative(columns=1)
                return
            self.insert(bookend_start + bookend_end)
            self.move_cursor_relative(columns=-1)
        else:
            selection = self.selection
            text = bookend_start + self.selected_text + bookend_end
            self.replace(text, selection.start, selection.end)
            # self.selection = (selection.start, selection.end + len(bookend_end + bookend_start))

    def _next_cell(self, forwards: bool) -> bool:
        text = self.get_text_range(self.get_cursor_line_start_location(), self.cursor_location)

        if not self.selected_text == "":
            return False

        if not text.startswith("|"):
            return False

        # if in markdown table go to next cell
        if not self.language == "markdown":
            return False

        cursor = self.cursor_location
        if forwards:
            start = (cursor[0], cursor[1] + 1)
            end = self.get_cursor_line_end_location()
        else:
            start = self.get_cursor_line_start_location()
            end = (cursor[0], cursor[1] - 1)

        text = self.get_text_range(start, end)
        # find next pipe
        if forwards:
            match = re.search(r"\|", text)
            if match:
                space = 3
                match_start = match.start() + space
                self.move_cursor_relative(columns=match_start)
                # self.notify(f"Moving cursor forward to {match_start}. Searched from {str(start)} to {str(end)}")
                return True
        else:
            # When moving backwards, we need to find the pipe that comes before the cursor's current position
            start = self.get_cursor_line_start_location()
            end = (cursor[0], cursor[1] - 1)

            # Extract the text range for searching
            text_before_cursor = self.get_text_range(start, end)

            # Find the last pipe in the text before the cursor
            match = re.search(r"\|(?=[^\|]*$)", text_before_cursor)
            if match:
                # Calculate the position of the cursor relative to the start of the line
                match_pos = match.start()

                # Move cursor to the left of the matched pipe character
                # We subtract from the cursor's current column position the difference
                # between the match position and the end column position of the text before the cursor
                cursor_move_distance = match_pos - end[1]
                self.move_cursor_relative(columns=cursor_move_distance)
                self.notify(f"Moving cursor backwards to {cursor_move_distance}. Searched from {str(start)} to {str(end)}")
                return True

        self.notify(f"No match from {str(start)} to {str(end)}")
        return False

    def _whitespace(self, spaces: int) -> None:
        start_location = self.get_cursor_line_start_location()

        if spaces < 0:
            spaces = abs(spaces)
            if self.selected_text == "":
                text = self.get_text_range(start_location, self.cursor_location)
                # remove leading whitespace from text up to spaces number if whitepsace exists
                if text.startswith(" " * spaces):
                    text = text[spaces:]
                    self.replace(text, start_location, self.cursor_location)
                    return
                elif text.startswith("\t"):
                    text = text[1:]
                    self.replace(text, start_location, self.cursor_location)
                    return
            else:
                selection = self.selection
                lines = self.selected_text.split("\n")
                new_lines = []
                for line in lines:
                    if line.startswith(" " * spaces):
                        new_lines.append(line[spaces:])
                    else:
                        new_lines.append(line)
                text = "\n".join(new_lines)
                self.replace(text, selection.start, selection.end)
                # self.selection.end = (selection.end[0], selection.end[1] - spaces)
            return

        if self.selected_text == "":
            before_cursor = self.get_text_range(self.get_cursor_line_start_location(), self.cursor_location)
            # check to see if - exists with arbitrary whitespace before
            if re.match(r"\s*-\s", before_cursor):
                self.insert((" " * spaces), start_location)
                self.notify("Match")
                return

            self.insert(" " * spaces)
        else:
            selection = self.selection
            lines = self.selected_text.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(" " * spaces + line)
            text = "\n".join(new_lines)
            self.replace(text, selection.start, selection.end)

    def _continue_list(self, this_line) -> None:
        # if - or 1. continue list with same amount of whitespace as found string
        leading_whitespace = re.match(r"(\s*)", this_line).group(1)

        match = re.match(r"\s*-\s\[\s\]\s[^\s]*", this_line)  # Check for todo list
        if match:
            return f"\n{leading_whitespace}- [ ] "

        # Determine the type of list from the previous line
        match = re.match(r"\s*(\d+)\.\s[^\s]", this_line)  # Check for numbered list
        if match:
            next_number = int(match.group(1)) + 1
            return f"\n{leading_whitespace}{next_number}. "

        match = re.match(r"\s*-\s[^\s]", this_line)  # Check for bulleted list
        if match:
            return f"\n{leading_whitespace}- "

        # Regular expression to match a markdown table row
        table_row_re = re.compile(r"^\s*\|?(?:[^\|]*\|)+[^\|]*\|?\s*$")

        # check if next line can be calculated

        if self.cursor_location[0] != self.get_cursor_down_location()[0]:
            # Get the start and end locations of the next line
            next_start = self.get_cursor_line_start_location()
            next_start = (next_start[0] + 1, next_start[1])
            next_end = self.get_cursor_line_end_location()
            next_end = (next_end[0] + 1, next_end[1])

            # Retrieve the next line of text
            next_line = self.get_text_range(next_start, next_end)

            # Notify about the next line - for debugging purposes
            # self.notify(f"Next line: {next_line}")
            next_line_match = table_row_re.match(next_line)
        else:
            next_line_match = False

        # #TODO: Hack
        this_line = self.document.get_line(self.cursor_location[0])

        # Check if the previous line is a table row and the next line is not
        if table_row_re.match(this_line) and not next_line_match:
            # Split the previous line into columns, taking into account leading and trailing spaces within the cells
            # We also maintain the outer spaces outside the first and last pipe
            leading_spaces = this_line[: this_line.find("|")]
            trailing_spaces = this_line[this_line.rfind("|") + 1 :]
            columns = this_line.strip().split("|")[1:-1]  # Exclude the first and last empty elements after strip

            # Create a new row that maintains the same spacing as the previous row's columns
            new_row = leading_spaces + "\n|" + "|".join(" " * len(col) for col in columns) + "|" + trailing_spaces
            self.insert(new_row, (self.cursor_location[0], len(self.document.lines[self.cursor_location[0]])))
            return None

        # Check if the next line is a table row
        elif next_line_match:
            # Assuming you are in a table and next_line_match is True, indicating the next line is also a table row

            # Get the content of the current line up to the cursor's column position
            current_cursor_row, current_cursor_column = self.cursor_location
            current_line_start = (current_cursor_row, 0)
            current_line_up_to_cursor = self.get_text_range(current_line_start, self.cursor_location)

            # Count the number of pipes (cells) before the cursor on the current line to find the cell index
            cell_index = current_line_up_to_cursor.count("|")

            # Move the cursor down one row
            self.move_cursor_relative(rows=1)

            # Now retrieve the content of the next line
            next_line_start = (current_cursor_row + 1, 0)
            next_line_end = self.get_cursor_line_end_location()
            next_line_end = (next_line_end[0] + 1, next_line_end[1])
            next_line = self.get_text_range(next_line_start, next_line_end)

            # Find the position of the same cell in the next line by finding the nth pipe
            # corresponding to the cell index
            pipe_count = 0
            column_position = 0
            for char in next_line:
                if char == "|":
                    pipe_count += 1
                if pipe_count == cell_index:
                    break
                column_position += 1

            # Now we have the column position of the pipe that marks the beginning of the target cell in the next line
            # We move the cursor to the right of that pipe, which should be the start of the cell
            # We need to add 1 to position the cursor inside the cell, right after the pipe
            self.move_cursor_relative(columns=column_position - current_cursor_column + 1)

            return None

        return "\n"

    def _newline(self) -> None:
        start_location = self.get_cursor_line_start_location()
        previous_line = self.get_text_range(start_location, self.cursor_location)

        # If the previous line is a list, continue the list
        ret = self._continue_list(previous_line)
        if ret != None:
            self.insert(ret)
            return

    def _on_key(self, event: events.Key) -> None:
        # self.notify(f"{event.character}  |  {event.aliases}")

        if event.character == "(":
            self._insert_bookend_pair("(", ")")
            event.prevent_default()
        elif event.character == "[":
            self._insert_bookend_pair("[", "]")
            event.prevent_default()
        elif event.character == "{":
            self._insert_bookend_pair("{", "}")
            event.prevent_default()
        elif event.character == "'":
            self._insert_bookend_pair("'", "'")
            event.prevent_default()
        elif event.character == '"':
            self._insert_bookend_pair('"', '"')
            event.prevent_default()
        elif event.character == "`":
            self._insert_bookend_pair("`", "`")
            event.prevent_default()
        elif event.character == "<":
            self._insert_bookend_pair("<", ">")
            event.prevent_default()
        elif event.character == "~":
            self._insert_bookend_pair("~", "~", only_selection=True)
            event.prevent_default()
        elif event.character == "*":
            self._insert_bookend_pair("*", "*", only_selection=True)
            event.prevent_default()

        elif "shift+tab" in event.aliases:
            if not self._next_cell(False):
                self._whitespace(-4)
            event.prevent_default()

        elif event.character == "\t":
            if not self._next_cell(True):
                self._whitespace(4)
            event.prevent_default()

        elif "shift+enter" in event.aliases:
            regex = table_row_re = re.compile(r"^\s*\|?(?:[^\|]*\|)+[^\|]*\|?\s*$")
            if regex.match(self.get_text_range(self.get_cursor_line_start_location(), self.get_cursor_line_end_location)):
                self.move_cursor_relative(rows=-11)

        # if enter in list of aliases
        elif "enter" in event.aliases:
            self._newline()
            event.prevent_default()


class Noteri(App):
    CSS_PATH = "noteri.tcss"
    COMMANDS = App.COMMANDS | {FileCommands} | {WidgetCommands}
    BINDINGS = [
        Binding("ctrl+n", "new", "New File"),
        Binding("ctrl+s", "save", "Save File"),
        Binding("shift+ctrl+s", "save_as", "Save As"),
        Binding("ctrl+r", "rename", "Rename File"),
        Binding("ctrl+d", "delete", "Delete File"),
        Binding("ctrl+shift+x", "cut", "Cut Text", priority=True),
        # Binding("ctrl+shift+c", "copy", "Copy Text", priority=True),
        Binding("ctrl+y", "copy", "Copy Text", priority=True),
        Binding("ctrl+shift+v", "paste", "Paste Text", priority=True),
        Binding("ctrl+v", "paste", "Paste Text", priority=True),
        Binding("ctrl+f", "find", "Find Text", priority=True),
        Binding("ctrl+t", "table", "Create Table"),
        Binding("ctrl+shift+t", "bullet_list", "Create Bullet List"),
        Binding("ctrl+shift+n", "numbered_list", "Create Numbered List"),
        Binding("ctrl+shift+b", "block_quote", "Create Block Quote"),
        Binding("ctrl+shift+k", "create_link", "Create Link"),
        Binding("ctrl+shift+l", "copy_link", "Copy Link"),
        Binding("ctrl+shift+h", "horizontal_rule", "Create Horizontal Rule"),
        Binding("ctrl+b", "bold", "Bold Text"),
        Binding("ctrl+i", "italic", "Italic Text"),
        Binding("ctrl+1", "heading", "Heading 1"),
        Binding("ctrl+2", "heading", "Heading 2"),
        Binding("ctrl+3", "heading", "Heading 3"),
        Binding("ctrl+4", "heading", "Heading 4"),
        Binding("ctrl+5", "heading", "Heading 5"),
        Binding("ctrl+6", "heading", "Heading 6"),
        Binding("ctrl+y", "redo", "Redo"),
        Binding("ctrl+z", "undo", "Undo"),
        # Binding("ctrl+shift+c", "copy", "Copy Text", priority=True),
        # Binding("ctrl+shift+v", "paste", "Paste Text", priority=True),
    ]

    class FileSystemCallback(Event):
        def __init__(self, callback, input):
            super().__init__()
            self.callback = callback
            self.input = input

    def __init__(self, path="./"):
        super().__init__()

        self.directory = "./"
        self.filename = None
        self.languages = []
        self.clipboard = ""
        self.unsaved_changes = False
        self.action_stack = []
        self.selected_directory = self.directory
        self.backlinks = []
        self.history_index = 0
        self.history = []
        self.history_disabled = False
        self.history_counter = 0
        self.markdown_updates = []
        self.write_lock = threading.Lock()
        self.unprinted_changes = True
        self.unprinted_footer = True
        self.last_find = ""

        self.expand_lock = threading.Lock()
        self.allowed_to_expand = True

        path = Path(path)
        if path.is_file():
            self.filename = path

            # TODO: Path too

        elif path.is_dir():
            self.directory = path
            self.selected_directory = path

    def compose(self) -> ComposeResult:
        self.ta = ExtendedTextArea(id="text_area")
        if get_language:
            for scm_file in SCM_PATH.glob("*.scm"):
                self.app.ta.register_language(get_language(scm_file.stem), scm_file.read_text())
        self.markdown = Markdown(id="markdown")
        # self.table_of_contents = Markdown(id="table_of_contents")

        # Find  Binding("ctrl+x", "delete_line", "delete line", show=False) in self.ta., and remove it
        self.app.ta.BINDINGS = [b for b in self.ta.BINDINGS if b.key != "ctrl+x"]
        self.app.ta.action_delete_line = self.action_cut
        self.app.ta.delete_word_right = self.action_find
        # with Vertical():
        with Horizontal():
            yield DirectoryTree(self.directory)
            yield self.ta
            with Vertical(id="md"):
                yield Markdown("", id="title")
                with ScrollableContainer(id="scrollable_markdown"):
                    # yield self.table_of_contents
                    yield self.markdown
                    yield Markdown(id="backlinks")
                    # yield RadioButton(id="todo")

        yield Label(id="footer")

    def on_mount(self):
        self.ta.focus()
        self.query_one("#markdown", expect_type=Markdown).display = False
        self.open_file(self.filename)
        self.dt = self.query_one("DirectoryTree", expect_type=DirectoryTree)
        self.refresh_directory_tree()
        self.print_footer()
        # self.query_one("#radio_buttons", expect_type=RadioButton).display = False
        self.run_worker(self._update_markdown_worker, exit_on_error=True, thread=False)
        self.run_worker(self._update_footer_worker, exit_on_error=True, thread=False)

    async def _update_footer_worker(self):
        while self.app.is_running:
            if self.unprinted_footer:
                unsaved_char = ""
                if self.unsaved_changes:
                    unsaved_char = "*"

                filename = self.filename
                if self.filename is None:
                    filename = "New File"

                language = self.ta.language

                if language is None:
                    language = "Plain Text"

                selected_text = self.ta.selected_text
                # calculate selection width
                cursor_width = ""
                if len(selected_text) > 0:
                    cursor_width = f" : {len(selected_text)}"

                cursor_location = self.ta.cursor_location
                self.query_one("#footer", expect_type=Label).update(
                    f"{self.selected_directory} | {unsaved_char}{filename} | {language} | {str(cursor_location)}{cursor_width}"
                )
                self.unprinted_footer = False

            # time.sleep(1)
            await asyncio.sleep(0.1)

    @work(thread=True, exclusive=True)
    def print_footer(self):
        self.unprinted_footer = True

    @textual.on(TextArea.SelectionChanged)
    def cursor_moved(self, event: TextArea.SelectionChanged) -> None:
        self.print_footer()

    @work(thread=True, exclusive=True)
    @textual.on(TextArea.Changed, "#text_area")
    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        self.history_counter += 1
        self.unsaved_changes = True

        # with self.write_lock:
        self.unprinted_changes = True
        # self.unprinted_changes = True
        if self.history_counter > 5:
            self.add_history()

    async def _update_markdown_worker(self):
        while self.app.is_running:
            if self.unprinted_changes:
                with self.write_lock:
                    if self.unprinted_changes:
                        self.unprinted_changes = False
                        self.call_next(self.markdown.update, self.ta.text)
            # time.sleep(2)
            await asyncio.sleep(0.1)

    @textual.on(DirectoryTree.FileSelected)
    def file_selected(self, event: DirectoryTree.FileSelected):
        with self.expand_lock:
            if not self.allowed_to_expand:
                return

        self.open_file(event.path)
        self.unsaved_changes = False

    @textual.on(DirectoryTree.DirectorySelected)
    def directory_selected(self, event: DirectoryTree.DirectorySelected):
        with self.expand_lock:
            if not self.allowed_to_expand:
                return
        self.selected_directory = event.path

    @textual.on(Markdown.LinkClicked)
    def linked_clicked(self, message: Markdown.LinkClicked):
        self.toggle_class("DirectoryTree")
        # read first character of path
        href = message.href
        if href[0] == "#":
            tag = href[1:].replace("%20", " ")
            if not self.markdown.goto_anchor(href[1:].replace("%20", " ")):
                self.notify(f"Anchor {tag} not found", severity="error", title="Anchor Not Found")
            return
        if href.startswith("http"):
            self.notify(f"Opening external link {href}")
            os.system(f"open {href}")
            return

        file_suffixs = [
            ".png",
            ".jpg",
            ".jpeg",
            ".tiff",
            ".gif",
            ".bmp",
            ".svg",
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".zip",
            ".tar",
            ".gz",
            ".tgz",
            ".rar",
            ".7z",
            ".mp3",
            ".mp4",
            ".wav",
            ".ogg",
            ".flac",
            ".avi",
            ".mov",
            ".wmv",
            ".mkv",
            ".webm",
            ".m4a",
            ".m4v",
            ".flv",
            ".mpeg",
            ".mpg",
            ".mpe",
            ".mp2",
            ".mpv",
            ".m2v",
            ".m4v",
            ".3gp",
            ".3g2",
            ".mxf",
            ".roq",
        ]

        for suffix in file_suffixs:
            if href.endswith(suffix):
                self.notify(f"Opening external file {self.filename.parent}/{href}")
                os.system(f'open "{self.filename.parent}/{href}"')
                return

        # get subdirectory of filepath
        # path = Path(self.filename).parent / href
        href = str(href).replace("%20", " ")
        if message.markdown.id == "backlinks":
            path = Path(href)
        else:
            path = Path(self.filename).parent / href

        self.open_file(path)

    def _update_backlinks_helper(self, path: Path):
        glob = list(Path(path).glob("./*"))

        for item in glob:
            if item.name[0] == ".":
                continue

            if item.is_dir():
                self._update_backlinks_helper(item)
            elif item.name.endswith(".md"):
                with open(item, "r") as f:
                    text = f.read()
                    if text.find(self.filename.name + ")") != -1:
                        self.backlinks.append(item)

    def update_backlinks(self):
        self.backlinks.clear()
        bl = self.query_one("#backlinks", expect_type=Markdown)
        self._update_backlinks_helper(self.directory)

        backlink_text = ""

        # TODO: Sort

        for item in self.backlinks:
            backlink_text += f"- [{item.name}]({str(item)})\n"

        if backlink_text != "":
            bl.display = True
            bl.styles.height = "auto"
        else:
            bl.display = False
            bl.styles.height = "0"

        backlink_text = "###\n### Backlinks\n" + backlink_text
        bl.update(backlink_text)

    def open_file(self, path: Path) -> None:
        if path == None:
            return
        if path.is_dir():
            return

        if self.unsaved_changes:
            self.action_stack.insert(0, partial(self.open_file, path))
            self.push_screen(
                YesNoPopup("Unsaved Changes", self.unsaved_changes_callback, message=f"Save Changes to {self.filename} ?")
            )
            return

        path = Path(path)

        try:
            with open(path) as f:
                text = f.read()
                self.ta.load_text(text)
                self.filename = path
                self.selected_directory = path.parent

        except FileNotFoundError as e:
            self.notify(f"File not found: {path}", severity="error", title="FileNotFoundError")
            return
        except UnicodeDecodeError as e:
            # self.notify(f"File is not a text file: {path}", severity="error", title="UnicodeDecodeError")
            os.system(f'open "{path}"')
            return

        file_extensions = {
            ".sh": "bash",
            ".css": "css",
            ".tcss": "css",
            ".html": "html",
            ".json": "json",
            ".md": "markdown",
            ".py": "python",
            ".regex": "regex",
            ".sql": "sql",
            ".toml": "toml",
            ".yaml": "yaml",
        }

        if path.suffix in file_extensions:
            try:
                self.ta.language = file_extensions[path.suffix]
            except LanguageDoesNotExist:
                self.notify(f"Issue loading {file_extensions[path.suffix]} language.", title="Language Error", severity="error")
                self.ta.language = None
            except NameError:
                self.notify(f"Issue loading {file_extensions[path.suffix]} language.", title="Language Error", severity="error")
                self.ta.language = None
        else:
            self.ta.language = None

        md = self.query_one("#markdown", expect_type=Markdown)
        title = self.query_one("#title", expect_type=Markdown)
        backlinks = self.query_one("#backlinks", expect_type=Markdown)

        if path.suffix == ".md":
            md.display = True
            title.display = True
            backlinks.display = True
            md.update(text)
            title.update("## " + str(self.filename.parts[-1])[:-3])
            self.update_backlinks()

        else:
            title.display = False
            md.display = False
            backlinks.display = False

        self.history.clear()
        self.history_index = 0
        self.add_history()

        self.configure_widths()

        self.unsaved_changes = False
        self.unprinted_footer = True
        self.unprinted_changes = True

    def toggle_widget_display(self, id):
        widget = self.query_one(id)

        if widget.display:
            widget.display = False
        else:
            widget.display = True

        self.configure_widths()

    def configure_widths(self):
        # if both enabled set width to 50%
        # if one enabled set to 100% and 0%
        # if both disabled set to 0%

        markdown = self.query_one("#markdown")
        md = self.query_one("#md")
        title = self.query_one("#title")
        backlinks = self.query_one("#backlinks")

        ta = self.ta

        if markdown.display and self.ta.display:
            md.styles.width = "50%"
            self.ta.styles.width = "50%"
        elif markdown.display:
            md.styles.width = "100%"
            self.ta.styles.width = "0"
        elif self.ta.display:
            md.styles.width = "0"
            self.ta.styles.width = "100%"
        else:
            md.styles.width = "0"
            self.ta.styles.width = "0"

        # TODO: Cooler way of doing this
        md.display = markdown.display
        title.display = markdown.display
        backlinks.display = markdown.display

    # def _refresh_directory_tree_helper(self, search_text, node):
    #     if node.data.path.is_dir():
    #         for child in node.children:
    #             self._refresh_directory_tree_helper(search_text, child)
    #     else:
    #         if search_text == "":
    #             node.display = True
    #         else:
    #             if search_text in node.data.path.name:
    #                 node.display = True
    #             else:
    #                 node.display = False

    @work(exclusive=True)
    async def refresh_directory_tree(self):
        with self.expand_lock:
            self.allowed_to_expand = False

        # self.dt.root.toggle_all()

        node = self.dt.cursor_node
        line = self.dt.cursor_line
        self.notify(f"Child len {len(self.dt.children)}")

        await self.dt.reload_node(self.dt.root)

        # self.dt.root.toggle_all()

        # node = self.dt.get_node_by_id(id)
        node = self.dt.get_node_at_line(line)

        if node != None:
            self.dt.select_node(node)
        else:
            self.notify(f"Could not find id {line}")
            self.notify(f"Child len {len(self.dt.children)}")

        with self.expand_lock:
            self.allowed_to_expand = True

    def new_file(self, file_name):
        with open(file_name, "w") as f:
            f.write("")
        self.refresh_directory_tree()
        self.open_file(Path(file_name))
        self.notify(f"Created {file_name}", title="Created")

    def save_file(self, new_filename=None):
        if self.filename is None and new_filename is None:
            self.action_save_as()
            return

        filename = self.filename if new_filename is None else new_filename

        with open(filename, "w") as f:
            f.write(self.ta.text)
        self.notify(f"Saved {filename}", title="Saved")
        self.filename = filename

        self.refresh_directory_tree()

        self.unsaved_changes = False
        self.unprinted_footer = True
        self.unprinted_changes = True

    def delete_file(self):
        if self.dt.cursor_node.data.path.is_dir():
            if shutil.rmtree.avoids_symlink_attacks:
                shutil.rmtree(self.dt.cursor_node.data.path)
        else:
            os.remove(self.dt.cursor_node.data.path)
        self.notify(f"Deleted {self.dt.cursor_node.data.path}", title="Deleted")
        self.refresh_directory_tree()

    def new_directory(self, directory_name):
        os.mkdir(directory_name)
        self.refresh_directory_tree()
        self.notify(f"Created {directory_name}", title="Created")

    def rename_file(self, new_filename):
        path = self.dt.cursor_node.data.path
        if new_filename == path:
            return

        if path.is_dir():
            # move directory
            os.rename(str(path), new_filename)
            self.dt.watch_path()
        elif path.is_file():
            tmp = self.filename
            self.save_file(new_filename)
            os.remove(tmp)
            self.dt.watch_path()
        return

    def create_table(self, rows, columns, header):
        self.add_history()

        self.history_counter
        insert_text = ""
        if header:
            insert_text += f"|   {'|   '.join([''] * columns)}|\n"
            insert_text += f"|{'|'.join(['---'] * columns)}|\n"

        for i in range(rows):
            row_text = f"|   {'|   '.join([''] * columns)}|\n"
            insert_text += row_text

        self.ta.replace(insert_text, self.ta.selection.start, self.ta.selection.end)

    def cleanup_table(self):
        md_table = self.ta.selected_text

        if md_table == "":
            return
        if md_table == None:
            return

        lines = md_table.strip().split("\n")
        header_cols = lines[0].split("|")[1:-1]
        matrix = [line.split("|")[1:-1] for line in lines[2:]]
        matrix = [[cell.strip() for cell in row] for row in matrix if any(cell.strip() for cell in row)]
        matrix.insert(0, [col.strip() for col in header_cols])  # Include headers in the matrix for width calculation
        matrix_transposed = list(zip(*matrix))
        matrix_transposed = [col for col in matrix_transposed if any(cell for cell in col)]
        matrix = list(zip(*matrix_transposed))

        # Calculate column widths based on the widest content in each column
        col_widths = [max(len(cell) for cell in col) for col in matrix_transposed]

        # Centering content in each cell
        def center_cell(cell, width):
            padding_total = max(width - len(cell), 0)
            padding_left = padding_total // 2
            padding_right = padding_total - padding_left
            return " " * padding_left + cell + " " * padding_right

        rebuilt_table = [
            "| " + " | ".join(center_cell(cell, width) for cell, width in zip(row, col_widths)) + " |" for row in matrix[1:]
        ]  # Exclude header row
        rebuilt_header = "| " + " | ".join(center_cell(cell, width) for cell, width in zip(matrix[0], col_widths)) + " |"
        rebuilt_separator = "|-" + "-|-".join("-" * width for width in col_widths) + "-|"
        clean_table = "\n".join([rebuilt_header, rebuilt_separator] + rebuilt_table)

        self.ta.replace(clean_table, self.ta.selection.start, self.ta.selection.end)

    def unsaved_changes_callback(self, value):
        if value:
            self.save_file()
        self.unsaved_changes = False
        self.action_stack.pop()()

    def delete_file_callback(self, value):
        if value:
            self.delete_file()

    def action_new(self):
        self.push_screen(
            InputPopup(self.new_file, title="New File", validators=[Length(minimum=1)], default=str(self.selected_directory) + "/")
        )

    def action_new_directory(self):
        self.push_screen(
            InputPopup(
                self.new_directory,
                title="New Directory",
                validators=[Length(minimum=1)],
                default=str(self.selected_directory) + "/",
            )
        )

    def action_save(self):
        self.save_file()

    def action_save_as(self):
        self.push_screen(InputPopup(self.save_file, title="Save As", validators=[Length(minimum=1)]))

    def action_rename(self):
        path = self.dt.cursor_node.data.path
        self.push_screen(InputPopup(self.rename_file, title="Rename", validators=[Length(minimum=1)], default=str(path)))

    def action_delete(self):
        self.push_screen(YesNoPopup(f"Delete {self.dt.cursor_node.data.path}", self.delete_file_callback))

    def action_copy(self):
        self.clipboard = self.ta.selected_text
        if pyperclip:
            pyperclip.copy(self.clipboard)
            self.notify(f"{self.clipboard}", title="Copied")

    def action_cut(self):
        self.action_copy()

        self.ta.delete(self.ta.selection.start, self.ta.selection.end)

    def action_paste(self):
        if pyperclip:
            self.ta.replace(pyperclip.paste(), self.ta.selection.start, self.ta.selection.end)
        else:
            self.ta.replace(self.clipboard, self.ta.selection.start, self.ta.selection.end)

    def action_table(self):
        if self.ta.selected_text != "":
            self.cleanup_table()
            return
        self.push_screen(MarkdownTablePopup(self.create_table, validators=[Length(minimum=1)]))

    def generate_table_of_contents(self, table_of_contents):
        # _table_of_contents is (level, id, block_number)
        table_of_contents_lines = []
        previous_level = 1
        self.notify(str(table_of_contents))
        slugs = TrackedSlugs()
        for header in table_of_contents:
            level = header[0]
            id = header[1]
            block_number = header[2]
            if previous_level < level - 1:
                for l in range(previous_level, level - 1):
                    table_of_contents_lines.append(f"{'  '* (l - 1)}- ")

            # github slug
            tag = slugs.slug(id)
            table_of_contents_lines.append(f"{'  ' * (level - 1)}- [{id}](#{tag})")
            previous_level = level

        return "\n".join(table_of_contents_lines)

    def action_table_of_contents(self):
        self.ta.replace(
            self.generate_table_of_contents(self.markdown._table_of_contents),
            self.ta.selection.start,
            self.ta.selection.end,
            maintain_selection_offset=False,
        )
        # get all links

    def action_directory_table_of_contents(self):
        # generate a links to all files in directory, not including the current file

        lines = []

        # get all files in directory
        for file in self.selected_directory.glob("./*"):
            if file.is_dir():
                continue
            if file.name == self.filename.name:
                continue
            if file.name.endswith(".md"):
                file_link = str(file.name).replace(" ", "%20")
                lines.append(f"- [{file.name}]({file_link})")
        self.ta.replace("\n".join(lines), self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False)

    def action_bullet_list(self):
        # in area selected, add a bullet to each line if it doesn't already exist
        lines = self.ta.selected_text.split("\n")
        refactored_lines = []
        for line in lines:
            # Check if the line already starts with a bullet
            if not line.startswith("- "):
                line = f"- {line}"
            refactored_lines.append(line)

        self.ta.replace(
            "\n".join(refactored_lines), self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def action_numbered_list(self):
        # In area selected, add "1. " to each line if not already numbered and not whitespace
        lines = self.ta.selected_text.split("\n")
        refactored_lines = []
        for line in lines:
            # Check if the line is not just whitespace and doesn't already start with a number followed by a dot and a space
            if line.strip() and not line.lstrip().startswith(tuple(f"{i}." for i in range(1, 10))):
                line = f"1. {line}"
            refactored_lines.append(line)

        self.ta.replace(
            "\n".join(refactored_lines), self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def action_block_quote(self):
        refactored_lines = []
        # If there is a selection, wrap it in a code block
        for line in self.ta.selected_text.split("\n"):
            if not line.startswith(">"):
                line = f"> {line}"
            refactored_lines.append(line)
        self.ta.replace(
            "\n".join(refactored_lines), self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def action_code_block(self):
        # If there is a selection, wrap it in a code block
        if self.ta.selected_text != "":
            self.ta.replace(f"```\n{self.ta.selected_text}\n```", self.ta.selection.start, self.ta.selection.end)
            return

    def action_create_link(self):
        self.create_link()

    def action_bold(self):
        self.ta.replace(
            f"**{self.ta.selected_text}**", self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def action_italic(self):
        self.ta.replace(
            f"*{self.ta.selected_text}*", self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def action_horizontal_rule(self):
        self.ta.replace(f"---", self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False)

    def action_heading(self, level):
        self.ta.replace(
            f"{'#' * level} {self.ta.selected_text}",
            self.ta.selection.start,
            self.ta.selection.end,
            maintain_selection_offset=False,
        )

    def action_find(self):
        self.app.push_screen(InputPopup(self.find_text, title="Find", validators=[Length(minimum=1)], default=self.last_find))
        pass

    def action_strikethrough(self):
        self.ta.replace(
            f"~~{self.ta.selected_text}~~", self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False
        )

    def find_text(self, search_text):
        self.last_find = search_text

        cursor_location = self.ta.cursor_location

        # calculate the string index from a row collumn on newlines.

        text = self.ta.text
        split_lines = text.split("\n")

        # calculate lenths of each line and stop before greater than selection row
        col = -1
        row = -1
        tmp_find_col = -1
        split_lines[cursor_location[0]] = split_lines[cursor_location[0]][cursor_location[1] + 1 :]
        for i, line in enumerate(split_lines[cursor_location[0] :]):
            tmp_find_col = line.find(search_text)
            if tmp_find_col != -1:
                if i == 0:
                    tmp_find_col += cursor_location[1] + 1
                col = tmp_find_col
                break
        row = i + cursor_location[0]

        if col == -1:
            self.notify(f"Reached bottom of doc searching for {search_text}.")
            return

        else:
            self.ta.move_cursor((row, col))
            self.ta.move_cursor_relative(columns=len(search_text), select=True)

    def action_copy_link(self):
        # put link into clipboard
        text = f"[{self.filename.name}]({self.filename})"
        pyperclip.copy(self.ta.selected_text)

    def add_history(self):
        if self.history_disabled:
            return

        ta = self.query_one("TextArea", TextArea)
        if self.history_index < len(self.history) - 1:
            self.history[self.history_index] = {"text": self.ta.text, "cursor_location": self.ta.cursor_location}
            # remove forward history
            self.history = self.history[: self.history_index + 1]
            # self.notify("Remove forward history")
        else:
            self.history.append({"text": self.ta.text, "cursor_location": self.ta.cursor_location})
        self.history_index += 1
        self.history_counter = 0
        # self.notify(f"add history. {self.history_index} {len(self.history)}")

        # make self.history only latest 10
        if len(self.history) > 10:
            self.history = self.history[-10:]
            self.history_index = 9

    def action_undo(self):
        # self.notify(f"Index: {self.history_index} Len History: {len(self.history)}")

        if self.history_index > 0:
            self.history_index -= 1
            self.history_disabled = True
            self.add_history()
            self.ta.load_text(self.history[self.history_index]["text"])
            self.ta.cursor_location = self.history[self.history_index]["cursor_location"]
            self.history_counter = -1

        self.history_disabled = False

        if self.history_index == 0:
            self.add_history()

    def action_redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.history_disabled = True
            self.ta.load_text(self.history[self.history_index]["text"])
            self.ta.cursor_location = self.history[self.history_index]["cursor_location"]
            self.history_counter = -1
        self.history_disabled = False

    def create_link(self, link: str = None, message=None, relative=True):
        if link == None:
            # TODO: Fuzzy match existing files
            if self.ta.selected_text.startswith("htt") or self.ta.selected_text.startswith("#"):
                link = self.ta.selected_text
            elif self.ta.selected_text.endswith(".md"):
                link = self.ta.selected_text
            else:
                link = ""

        if str(link).endswith(".md") and relative:
            link_path = Path(link)

            try:
                self.notify(f"{self.selected_directory}\n{link_path}")
                link = link_path.relative_to(self.selected_directory)
            except ValueError as e:
                self.notify(f"Could not find relative path for {link_path}, using abs")
                link = self.ta.selected_text

        if message == None and str(link).endswith(".md"):
            message = str(Path(link).name)[:-3]

        if message == None:
            if self.ta.selected_text == "":
                message = ""
            else:
                message = self.ta.selected_text

        self.ta.replace(f"[{message}]({link})", self.ta.selection.start, self.ta.selection.end, maintain_selection_offset=False)

    @textual.on(FileSystemCallback)
    def callback_message(self, message: FileSystemCallback):
        message.callback(*message.input)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path", default="./", nargs="?", help="Path to file or directory to open")
    args = parser.parse_args()

    app = Noteri(args.path)

    loop = asyncio.get_event_loop()
    try:
        if sys.platform in ("emscripten", "wasi"):
            for f in Path(".").glob("*.whl"):
                os.unlink(f)

            print(" ===================================== ")

            async with app.run_test(headless=True, size=(100, 32)) as pilot:
                while not loop.is_closed():
                    await asyncio.sleep(0.016)
        else:
            await app.run_async()

    except asyncio.exceptions.CancelledError:
        print("Cancelled")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
    finally:
        pass

