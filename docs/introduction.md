
## How does it work?

**qlm** is a lightweight python library that makes it easy to take beautiful notes on the command line.

It uses [Rich's](https://rich.readthedocs.io/en/stable/introduction.html) markdown rendering to make stuff look good in
your  terminal and uses the [Typer](https://github.com/tiangolo/typer) library for building command line apps in Python.

**qlm** also uses Github as a backend, so you can access your notes on any machine - you just need your Github
[Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

Your notes will be private by default and you can edit them easily - they're just files in a Github repository.

**qlm** provides a few commands to interact with the Github API directly, which makes it fast and simple to set things
up.

:rocket:

## Why **qlm**?

If you're anything like me, you often have to switch between different machines for work. _Work laptop, dev laptop,
personal laptop, shell on server x, shell on container y, debug session in k8s pod z_.

And when you're in these situations, you want your notes! On the command line, and fast.

So that's what **qlm** does. I've found one other project like it - [Dnote](https://www.getdnote.com/) - which has some
very cool features. Check it out!

But it requires you to set up a SQL server or pay to use one, which is too much overhead for me. And it doesn't have
pretty markdown rendering.

:grin:

## Installation

<div id="termynal" data-termynal>
    <span data-ty="input">pip install qlm</span>
    <span data-ty="progress" data-ty-progressChar="·"></span>
    <span data-ty>Successfully installed qlm</span>
    <span data-ty="input">qlm --help</span>
</div>

## Set Up

To start taking notes, you should first connect to the github repository where you want to keep
them in the format `<username/repo>`.

Then, you can create, save and display notes in your terminal

:sunglasses:

<div id="termynal" data-termynal>
    <span data-ty="input">export qlm_token='your Github PAT token'</span>
    <span data-ty="input">qlm connect 'osintalex/notes'</span>
    <span data-ty="input">qlm config --local-repo 'folder to keep notes in'</span>
    <span data-ty="input">echo '# Example' > example.md</span>
    <span data-ty="input">qlm add example.md</span>
    <span data-ty="input">qlm show example.md</span>
</div>


## Offline Mode

**qlm** supports working offline. You can keep all your notes in a local folder, and then when you connect back online,
run `qlm publish` to add them to your remote.

<div id="termynal" data-termynal>
    <span data-ty="input">qlm offline 'folder to keep notes in'</span>
    <span data-ty="input">echo '# Example' > example.md</span>
    <span data-ty="input">qlm add example.md</span>
    <span data-ty="input">qlm connect 'username/repo'</span>
    <span data-ty="input">qlm publish</span>
</div>
