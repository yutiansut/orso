# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from typing import Iterable
from typing import Union

COLORS = {
    "\001OFFm": "\033[0m",  # Text Reset
    # Opteryx named colors
    "\001PUNCm": "\033[38;5;102m",
    "\001VARCHARm": "\033[38;5;229m",
    "\001CONSTm": "\033[38;5;117m",
    "\001NULLm": "\033[38;5;102m",
    "\001VALUEm": "\033[38;5;153m",
    "\001NUMERICm": "\033[38;5;212m",
    "\001DATEm": "\033[38;5;120m",
    "\001TIMEm": "\033[38;5;72m",
    "\001KEYm": "\033[38;5;183m",
    # an orange color - 222
    # a red color = 209
    # Regular Colors
    "\001BLACKm": "\033[0;30m",  # Black
    "\001REDm": "\033[0;31m",  # Red
    "\001GREENm": "\033[0;32m",  # Green
    "\001YELLOWm": "\033[0;33m",  # Yellow
    "\001BLUEm": "\033[0;34m",  # Blue
    "\001PURPLEm": "\033[0;35m",  # Purple
    "\001CYANm": "\033[0;36m",  # Cyan
    "\001WHITEm": "\033[0;37m",  # White
    # Bold
    "\001BOLD_BLACKm": "\033[1;30m",  # Black
    "\001BOLD_REDm": "\033[1;31m",  # Red
    "\001BOLD_GREENm": "\033[1;32m",  # Green
    "\001BOLD_YELLOWm": "\033[1;33m",  # Yellow
    "\001BOLD_BLUEm": "\033[1;34m",  # Blue
    "\001BOLD_PURPLEm": "\033[1;35m",  # Purple
    "\001BOLD_CYANm": "\033[1;36m",  # Cyan
    "\001BOLD_WHITEm": "\033[1;37m",  # White
    # Underline
    "\001UNDERLINE_BLACKm": "\033[4;30m",  # Black
    "\001UNDERLINE_REDm": "\033[4;31m",  # Red
    "\001UNDERLINE_GREENm": "\033[4;32m",  # Green
    "\001UNDERLINE_YELLOWm": "\033[4;33m",  # Yellow
    "\001UNDERLINE_BLUEm": "\033[4;34m",  # Blue
    "\001UNDERLINE_PURPLEm": "\033[4;35m",  # Purple
    "\001UNDERLINE_CYANm": "\033[4;36m",  # Cyan
    "\001UNDERLINE_WHITEm": "\033[4;37m",  # White
    # Background
    "\001BACKGROUND_BLACKm": "\033[40m",  # Black
    "\001BACKGROUND_REDm": "\033[41m",  # 	Red
    "\001BACKGROUND_GREE}m": "\033[42m",  # 	Green
    "\001BACKGROUND_YELLOWm": "\033[43m",  # 	Yellow
    "\001BACKGROUND_BLUEm": "\033[44m",  # 	Blue
    "\001BACKGROUND_PURPLEm": "\033[45m",  # 	Purple
    "\001BACKGROUND_CYANm": "\033[46m",  # 	Cyan
    "\001BACKGROUND_WHITEm": "\033[47m",  # 	White
}


def colorizer(record, can_colorize=True):
    if can_colorize:
        for k, v in COLORS.items():
            record = record.replace(k, v)
    else:
        for k, v in COLORS.items():  # pragma: no cover
            record = record.replace(k, "")

    return record


def html_table(dictset: Iterable[dict], limit: int = 5):  # pragma: no cover
    """
    Render the dictset as a HTML table.

    NOTE:
        This exhausts generators so is only recommended to be used on lists.

    Parameters:
        dictset: iterable of dictionaries
            The dictset to render
        limit: integer (optional)
            The maximum number of record to show in the table, defaults to 5

    Returns:
        string (HTML table)
    """

    def sanitize(htmlstring):
        ## some types need converting to a string first
        if isinstance(htmlstring, (list, tuple, set)) or hasattr(htmlstring, "as_list"):
            return "[ " + ", ".join([sanitize(i) for i in htmlstring]) + " ]"
        if hasattr(htmlstring, "items"):
            return sanitize("{ " + ", ".join([f'"{k}": {v}' for k, v in htmlstring.items()]) + " }")
        if not isinstance(htmlstring, str):
            return str(htmlstring)
        escapes = {'"': "&quot;", "'": "&#39;", "<": "&lt;", ">": "&gt;", "$": "&#x24;"}
        # This is done first to prevent escaping other escapes.
        htmlstring = htmlstring.replace("&", "&amp;")
        for seq, esc in escapes.items():
            htmlstring = htmlstring.replace(seq, esc)
        return htmlstring

    def _to_html_table(data, columns):
        yield '<table class="table table-sm">'
        for counter, record in enumerate(data):
            if counter == 0:
                yield '<thead class="thead-light"><tr>'
                for column in columns:
                    yield f"<th>{sanitize(column)}<th>\n"
                yield "</tr></thead><tbody>"

            yield "<tr>"
            for column in columns:
                sanitized = sanitize(record.get(column, ""))
                yield f"<td title='{sanitized}' style='max-width:320px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>{sanitized}<td>\n"
            yield "</tr>"

        yield "</tbody></table>"

    rows = []
    columns = []  # type:ignore
    i = -1
    for i, row in enumerate(iter(dictset)):
        rows.append(row)
        columns = columns + list(row.keys())
        if (i + 1) == limit:
            break
    columns = list(dict.fromkeys(columns))  # type:ignore

    import types

    footer = ""
    if isinstance(dictset, types.GeneratorType):
        footer = f"\n<p>top {i+1} rows x {len(columns)} columns</p>"
    elif hasattr(dictset, "__len__"):
        footer = f"\n<p>{len(dictset)} rows x {len(columns)} columns</p>"  # type:ignore

    return "".join(_to_html_table(rows, columns)) + footer


def ascii_table(
    table,
    limit: int = 5,
    display_width: Union[bool, int] = True,
    max_column_width: int = 30,
    colorize: bool = True,
):
    """
    Render the dictset as a ASCII table.

    NOTE:
        This exhausts generators so is only recommended to be used on lists.

    Parameters:
        dictset: iterable of dictionaries
            The dictset to render
        limit: integer (optional)
            The maximum number of record to show in the table, defaults to 5
        display_width: integer/boolean (optional)
            The maximum width of the table, if an integer, the number of characters,
            if a boolean, True uses the display width, False disables (5000)

    Returns:
        string (ASCII table)
    """

    if len(table) == 0:
        return "No data in table"

    # get the width of the display
    if isinstance(display_width, bool):
        if not display_width:  # pragma: no-cover
            display_width = 5000
        else:
            import shutil

            display_width = shutil.get_terminal_size((80, 20))[0]

    # Extract head data
    if limit > 0:
        t = table.slice(length=limit)
    else:
        t = table

    # width of index column
    index_width = len(str(len(table))) + 2

    def type_formatter(value, width):
        if value is None:
            return "\001NULLm" + "null".rjust(width)[:width] + "\001OFFm"
        if isinstance(value, bool):
            return "\001CONSTm" + str(value).rjust(width)[:width] + "\001OFFm"
        if isinstance(value, int):
            return "\001NUMERICm" + str(value).rjust(width)[:width] + "\001OFFm"
        if isinstance(value, float):
            return "\001NUMERICm" + str(value).rjust(width)[:width] + "\001OFFm"
        if isinstance(value, str):
            return "\001VARCHARm" + trunc_printable(str(value).ljust(width), width) + "\001OFFm"
        if isinstance(value, datetime.datetime):
            value = f"{value.strftime('%Y-%m-%d')} \001TIMEm{value.strftime('%H:%M:%S')}"
            return "\001DATEm" + trunc_printable(value.rjust(width), width) + "\001OFFm"
        if isinstance(value, list):
            value = (
                "\001PUNCm['\001VALUEm"
                + "\001PUNCm', '\001VALUEm".join(map(str, value))
                + "\001PUNCm']\001OFFm"
            )
            return trunc_printable(value, width)
        if isinstance(value, dict):
            value = (
                "\001PUNCm{"
                + "\001PUNCm, ".join(
                    f"'\001KEYm{k}\001PUNCm':'\001VALUEm{v}\001PUNCm'" for k, v in value.items()
                )
                + "}\001OFFm"
            )
            return trunc_printable(value, width)
        return str(value).ljust(width)[:width]

    def character_width(symbol):
        import unicodedata

        return 2 if unicodedata.east_asian_width(symbol) in ("F", "N", "W") else 1

    def trunc_printable(value, width, full_line: bool = True):
        offset = 0
        emit = ""
        ignoring = False

        for char in value:
            if char == "\n":
                emit += "\001PUNCm↵\001VARCHARm"
                offset += 1
                continue
            emit += char
            if char in ("\033", "\001"):
                ignoring = True
            if not ignoring:
                offset += character_width(char)
            if ignoring and char == "m":
                ignoring = False
            if not ignoring and offset >= width:
                return emit + "\001OFFm"
        line = emit + "\001OFFm"
        if full_line:
            return line + " " * (width - offset)
        return line

    def _inner():
        # Calculate width
        col_width = list(map(len, t.column_names))
        data_width = [
            max(list(map(len, map(str, [p for p in h if p is not None]))) + [4])
            for h in (t.collect(i) for i in range(t.columncount))
        ]
        col_width = [min(max(cw, dw), max_column_width) for cw, dw in zip(col_width, data_width)]

        # Print data
        data = [t.row(i) for i in range(len(t))]
        yield ("┌" + ("─" * index_width) + "┬─" + "─┬─".join("─" * cw for cw in col_width) + "─┐")
        yield (
            "│"
            + (" " * index_width)
            + "│ "
            + " │ ".join(v.ljust(w)[:w] for v, w in zip(t.column_names, col_width))
            + " │"
        )
        yield ("╞" + ("═" * index_width) + "╪═" + "═╪═".join("═" * cw for cw in col_width) + "═╡")
        for i in range(len(data)):
            formatted = [type_formatter(v, w) for v, w in zip(data[i], col_width)]
            yield ("│" + str(i + 1).rjust(index_width - 1) + " │ " + " │ ".join(formatted) + " │")
        yield ("└" + ("─" * index_width) + "┴─" + "─┴─".join("─" * cw for cw in col_width) + "─┘")

    return "\n".join(
        colorizer(trunc_printable(line, display_width, False), colorize) for line in _inner()
    )
