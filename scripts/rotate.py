import os
import subprocess
import sys
import textwrap
from string import Template

import toml

rotate_template = Template(
    textwrap.dedent("""\
        $logfile {
            daily
            rotate 7
            compress
            missingok
            notifempty
            copytruncate
            create 640 $whoami $whoami
            su $whoami $whoami
            postrotate
                systemctl --user restart $name.service
            endscript
        }
        """)
)


def mk_rotate():
    specific_name = sys.argv[1].strip() if len(sys.argv) == 2 else None

    with open("pyproject.toml", encoding="utf8") as f:
        pyproject = toml.load(f)
        pj_name = pyproject["project"]["name"]

    fname = pj_name if specific_name is None else specific_name

    # mk cache dir for log, *.conf, *.service
    # in case the user forgot to execute `rye run init`
    pwd = os.getcwd()
    cache_dir = os.path.join(pwd, "cache")
    os.makedirs(cache_dir, exist_ok=True)

    whoami = os.environ.get("USER", "")

    config = {
        "logfile": os.path.join(cache_dir, f"{fname}.log"),
        "whoami": whoami,
        "name": pj_name,
    }

    rotate_file = rotate_template.safe_substitute(config)
    print("\n", rotate_file)

    logratate = (
        subprocess.run("which logrotate", shell=True, capture_output=True)
        .stdout.decode("utf-8")
        .strip()
    )

    with open(
        os.path.join(
            cache_dir,
            f"{fname}.conf",
        ),
        "w",
        encoding="utf8",
    ) as f:
        f.write(rotate_file)

    # create logrotate-state file
    with open(
        os.path.join(cache_dir, ".logrotate-state"), "w", encoding="utf8"
    ) as f:
        pass

    crontab = "0 0 * * *"
    cron_cmd = textwrap.dedent(f"""\
        {crontab} cd {cache_dir} && \\
        {logratate} -state .logrotate-state {fname}.conf
    """)

    print(
        f"Please add this line to your crontab:\
        \n{cron_cmd}"
    )
