def display_table(
    cells, header=None, left_header=None, Id=None, header_style=None,
    footer=None,
):
    """
    cells: list of lists of str
    header: list of str
    left_header: list of str
    """
    nrows = len(cells)
    ncols0 = len(cells[0]) if len(cells) > 0 else 0
    ncols = len(header) if header is not None else ncols0
    for i, row in enumerate(cells):
        if len(row) != ncols:
            raise ValueError(f"row {i+1}/{nrows}: {len(row)} != {ncols}")
    _header_style = (
        "background-color: #ddd; " "text-align:right; " "padding: 0.1em"
    )
    header_style = header_style if header is not None else _header_style
    left_header_style = header_style
    cell_style = "text-align: right; padding: 0.4em 0em 0.4em 2em"

    o = f'<th style="{header_style}"></th>' if left_header is not None else ""
    if header is not None:
        for j in range(ncols):
            o += f'<th style="{header_style}">{header[j]}</th>'
    h = f"<thead><tr>{o}</tr></thead>"

    trs = ""
    for i in range(nrows):
        o = (
            f'<th style="{left_header_style}">{left_header[i]}</th>'
            if left_header
            else ""
        )
        for j in range(ncols):
            o += f'<td style="{cell_style}">{cells[i][j]}</td>'
        trs += f"<tr>{o}</tr>"
    if footer is not None:
        o = f'<th style="{header_style}"></th>' if left_header is not None else ""
        for j in range(ncols):
            o += f'<th style="{header_style}">{footer[j]}</th>'
        trs  += f"<tr>{o}</tr>"
    b = f"<tbody>{trs}</tbody>"
    _id = f'id="{Id}"' if Id is not None else ""
    t = f"<div {_id}><table>{h}{b}</table></div>"
    return t


def make_float(s, None_is_zero=True):
    none = 0.0 if None_is_zero else None
    if isinstance(s, str):
        if len(s.strip()) > 0:
            try:
                return float(s.strip())
            except ValueError:
                return none
        else:
            return none
    elif isinstance(s, (int, float)):
        return float(s)
    return none
