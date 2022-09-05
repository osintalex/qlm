# Reference

## `qlm --help` or `qlm`

**Usage**:

```console
$ [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add`: Add file(s) to your github remote
* `config`: Display and edit your current configuration
* `connect`: Checks if you can connect to github
* `create`: Creates and connects to a new repository
* `download`: Downloads your notes from a remote
* `edit`: Edit a file
* `get`: Download a file from your remote
* `ls`: Lists markdown files in your remote.
* `offline`: Switch to working in offline mode
* `publish`: Publishes files that were saved in offline
* `rm`: Removes a file
* `show`: Prints your file to the console

## `add`

Add file(s) to your github remote from your local repo. Accepts wildcards with glob syntax like
'*.md'.

If you're offline, qlm records this in your configuration. You can see which files qlm has stored by running
qlm config.

You can add them all to github later by running `qlm publish`.

You can empty this list of files by running `qlm config --empty-offline`. Or you can use
`git` yourself to send files to your remote!

**Usage**:

```console
$ add [OPTIONS] FILES
```

**Arguments**:

* `FILES`: The path to the file you want to add. Accepts wildcard syntax, i.e. myfolder/*.md  [required]

**Options**:

* `-f, --force`: Don't prompt before adding files  [default: False]
* `--help`: Show this message and exit.

## `config`

Display and edit your current configuration

**Usage**:

```console
$ config [OPTIONS]
```

**Options**:

* `-e, --editor TEXT`: The command to open the text editor you want to use, i.e. nano or vim
* `-eo, --empty-offline`: Empty the list of offline files to add with qlm publish. If you want more granular control of these files, it's probably best to empty them and then manually add them to them github using git on the command line  [default: False]
* `-lr, --local-repo TEXT`: The absolute path to the local directory you want to keep your files in.
* `-rr, --remote-repo TEXT`: The full name of the remote repo you want to use, i.e. username/repo
* `-hk, --hide-key TEXT`: Don't print out a specific key in the configuration output
* `-o, --offline TEXT`: Set offline to True or False. Defaults to True.  [default: True]
* `--help`: Show this message and exit.

## `connect`

Checks if you can connect to github and sets your config to online. You must set the environment variable
$qlm_token to connect.

You must specify the full name of the repo in the format username/repo. If you don't, qlm will attempt to find
the repo under your personal account username.

**Usage**:

```console
$ connect [OPTIONS] REMOTE
```

**Arguments**:

* `REMOTE`: The name of the remote github repository where your notes are, e.g. my-username/repo-name  [required]

**Options**:

* `--help`: Show this message and exit.

## `create`

Creates and connects to a new repository in github under your personal account. The repository is private by default
because privacy matters

**Usage**:

```console
$ create [OPTIONS] REPO_NAME
```

**Arguments**:

* `REPO_NAME`: The name of the new repo to create  [required]

**Options**:

* `-p, --public`: Make a public, not private repository  [default: False]
* `-f, --force`: Don't prompt before creating a new repo  [default: False]
* `--help`: Show this message and exit.

## `download`

Downloads your notes from a remote to a local repository. Online only command

To switch into online mode, run qlm connect.

**Usage**:

```console
$ download [OPTIONS] LOCAL
```

**Arguments**:

* `LOCAL`: The absolute path to where you want to keep your notes  [required]

**Options**:

* `-r, --remote TEXT`: The name of the remote you want to download files from. Defaults to whatever is in your config.
* `--help`: Show this message and exit.

## `edit`

Edit a file

Uses vim by default. You can change the text editor using qlm config --editor.

**Usage**:

```console
$ edit [OPTIONS] FILE
```

**Arguments**:

* `FILE`: The path to the file you want to edit relative to remote or local repo root.  [required]

**Options**:

* `--help`: Show this message and exit.

## `get`

Download a file from your remote

**Usage**:

```console
$ get [OPTIONS] FILE
```

**Arguments**:

* `FILE`: Path to the remote file you want to download  [required]

**Options**:

* `-r, --rename TEXT`: Rename the file you want to download
* `-d, --directory TEXT`: The local directory to save the file to. If not specified, qlm will download the file to your current working directory.
* `--help`: Show this message and exit.

## `ls`

Lists markdown files in your remote. Online only

To switch into online mode, run qlm connect.

**Usage**:

```console
$ ls [OPTIONS] [DIRECTORY]
```

**Arguments**:

* `[DIRECTORY]`: The directory you want to list the contents of. Defaults to the repo root if omitted.

**Options**:

* `-nm, --non-markdown`: Also list files that aren't markdown  [default: False]
* `--help`: Show this message and exit.

## `offline`

Switch to working in offline mode with a local directory

If you want to add your work to a remote later, use qlm publish.

**Usage**:

```console
$ offline [OPTIONS] LOCAL
```

**Arguments**:

* `LOCAL`: The absolute path to the local directory where you want to keep your notes  [required]

**Options**:

* `--help`: Show this message and exit.

## `publish`

Publishes files that were saved in offline mode using qlm add

**Usage**:

```console
$ publish [OPTIONS]
```

**Options**:

* `-f, --force`: Publish files without prompting for confirmation  [default: False]
* `--help`: Show this message and exit.

## `rm`

Removes a file

**Usage**:

```console
$ rm [OPTIONS] FILE
```

**Arguments**:

* `FILE`: The file you want to remove  [required]

**Options**:

* `-f, --force`: Remove the file without prompting for confirmation  [default: False]
* `--help`: Show this message and exit.

## `show`

Prints your file to the console. Looks much nicer if you use markdown

**Usage**:

```console
$ show [OPTIONS] FILE
```

**Arguments**:

* `FILE`: The path to the file you want see.  [required]

**Options**:

* `-nm, --no-markup`: Print a file out without rendering markdown.  [default: False]
* `--help`: Show this message and exit.
