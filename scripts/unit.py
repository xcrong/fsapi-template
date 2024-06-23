import os
import subprocess
import sys
import textwrap
from string import Template

import toml


def mk_unit():
    specific_name = sys.argv[1].strip() if len(sys.argv) == 2 else None

    unit_file_template = Template(
        textwrap.dedent("""\
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
    )

    pwd: str = os.getcwd()
    # mkdir for log
    os.makedirs(os.path.join(pwd, "cache"), exist_ok=True)

    rye = (
        subprocess.run("which rye", shell=True, capture_output=True)
        .stdout.decode("utf-8")
        .strip()
    )

    with open("pyproject.toml", encoding="utf8") as f:
        pyproject = toml.load(f)
        pj_name = pyproject["project"]["name"]

    pj_name = pyproject["project"]["name"]
    pj_description = pyproject["project"]["description"]

    cmd = input(
        f"ExecStart (Default: rye run \
            {'start' if specific_name is None else specific_name}): "
    ).strip()
    if not cmd:
        cmd = f"{rye} run {specific_name}"
    elif cmd.startswith("rye"):
        cmd = f"{rye} {cmd.removeprefix('rye ')}"

    description = input(f"Description (Default: {pj_description}): ").strip()
    if not description:
        description = pj_description

    config = {
        "description": description,
        "pwd": pwd,
        "cmd": cmd,
        "log": os.path.join(pwd, "cache", f"{pj_name}.log"),
    }

    unit_file = unit_file_template.safe_substitute(config)

    print("\n", unit_file)

    with open(
        f"{pj_name if specific_name is None else specific_name}.service",
        "w",
        encoding="utf8",
    ) as f:
        f.write(unit_file)