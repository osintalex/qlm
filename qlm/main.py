from typer import Typer

from qlm.commands import add, config, connect, create, download, edit, get, ls, offline, publish, rm, show

app: Typer = Typer(no_args_is_help=True, pretty_exceptions_show_locals=False, rich_markup_mode="rich")
app.command()(add)
app.command()(config)
app.command()(connect)
app.command()(create)
app.command()(download)
app.command()(edit)
app.command()(get)
app.command()(ls)
app.command()(offline)
app.command()(rm)
app.command()(publish)
app.command()(show)