import os
import toml
from string import Template


def mk_rotate():
    with open("pyproject.toml", "r", encoding="utf8") as f:
        pyproject = toml.load(f)
        pj_name = pyproject["project"]["name"]

    pwd = os.getcwd()
    whoami = os.environ.get("USER", "")

    rotate_template = Template("""\
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
}""")

    config = {
        "logfile": os.path.join(pwd, "cache", f"{pj_name}.log"),
        "whoami": whoami,
        "name": pj_name,
    }

    rotate_file = rotate_template.safe_substitute(config)

    print("\n", rotate_file)

    with open(f"{pj_name}.conf", "w", encoding="utf8") as f:
        f.write(rotate_file)

    print(
        f"Please add this line to your crontab:\n0 0 * * * /usr/sbin/logrotate {os.path.join(pwd, pj_name + '.conf')}"
    )
