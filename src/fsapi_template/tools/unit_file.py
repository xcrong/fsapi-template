import os
from string import Template

import toml


def mk_unit():
    unit_file_template = Template("""\
[Unit]
Description=$description
After=network.target

[Service]
WorkingDirectory=$pwd
ExecStart=$cmd
StandardOutput=append:$log
StandardError=inherit

[Install]
WantedBy=default.target
""")

    pwd: str = os.getcwd()
    home: str = os.path.expanduser("~")
    # mkdir for log
    os.makedirs(os.path.join(pwd, "cache"), exist_ok=True)

    with open("pyproject.toml", "r", encoding="utf8") as f:
        pyproject = toml.load(f)
        pj_name = pyproject["project"]["name"]
    pj_name = pyproject["project"]["name"]
    pj_description = pyproject["project"]["description"]

    cmd = input("ExecStart (Default: rye run start): ").strip()
    if not cmd:
        cmd = f"{home}/.rye/shims/rye run start"
    elif cmd.startswith("rye"):
        cmd = f"{home}/.rye/shims/{cmd}"

    description = input(f"Description (Default: {pj_description}): ").strip()
    if not description:
        description = "A template service for fastapi"

    config = {
        "description": description,
        "pwd": pwd,
        "cmd": cmd,
        "log": os.path.join(pwd, "cache", f"{pj_name}.log"),
    }

    unit_file = unit_file_template.safe_substitute(config)

    print("\n", unit_file)

    with open(f"{pj_name}.service", "w", encoding="utf8") as f:
        f.write(unit_file)
