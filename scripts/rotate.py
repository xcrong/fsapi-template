import os
import sys
import textwrap
from string import Template

import toml


def mk_rotate():
    specific_name = sys.argv[1].strip() if len(sys.argv) == 2 else None

    # mk cache dir for log, *.conf, *.service
    # in case the user forgot to execute `rye run init`
    pwd = os.getcwd()
    os.makedirs(os.path.join(pwd, "cache"), exist_ok=True)

    with open("pyproject.toml", encoding="utf8") as f:
        pyproject = toml.load(f)
        pj_name = pyproject["project"]["name"]

    whoami = os.environ.get("USER", "")

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

    config = {
        "logfile": os.path.join(pwd, "cache", f"{pj_name}.log"),
        "whoami": whoami,
        "name": pj_name,
    }

    rotate_file = rotate_template.safe_substitute(config)

    print("\n", rotate_file)

    with open(
        os.path.join(
            "cache",
            f"{pj_name if specific_name is None else specific_name}.conf",
        ),
        "w",
        encoding="utf8",
    ) as f:
        f.write(rotate_file)

    print(
        f"Please add this line to your crontab:\
        \n0 0 * * * /usr/sbin/logrotate {os.path.join(pwd, pj_name + '.conf')}"
    )
