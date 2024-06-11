# FastAPI Project Template

A template repository for a FastAPI project that can automatically generate Unit files for easy project management using Systemd to start, restart, and stop the project.

# How to Use?

## 1. Install rye

Rye is a necessary project management tool. You don't even need to install Python, but you do need rye.

Rye will manage itself and also manage the Python interpreter needed for the project.

This document assumes that the development and deployment environments are Linux. Installing the Python environment on Linux is very simple: `curl -sSf https://rye.astral.sh/get | bash`.

For more rye installation documentation, see: [https://rye.astral.sh/guide/installation/#installing-rye](https://rye.astral.sh/guide/installation/#installing-rye).

> You can still use this template for development on Windows. For installing rye, see the official website. All instructions in this document, except for the Unit file related parts, apply to the Windows environment.

## 2. Clone the project locally

```bash
cd ~
git clone https://github.com/xcrong/fsapi-template.git <project_name> # Replace with your desired project name
cd <project_name> 
```

## 3. Sync the environment

```bash
# Set up the environment
rye sync 
# Update project details
rye run project 
```

## 4. Develop the project

```bash
# During development, try hot-reloading the project, which by default monitors all *.py files and .envs files
rye run dev 
# Start the project
rye run start 
```

During project development, it is recommended to put all configurable items in environment variables, i.e., in the `.envs` file (please copy `.envs.example` to `.envs`).

These environment variables should be divided into two groups, one for controlling the program's behavior and the other for controlling `uvicorn`.

First, define the necessary environment variables in the `AppConfig` and `UnicornConfig` in `config.py`, and provide default values. If you need to change the default values or if no default values are set, you need to define them in the `.envs`.

Using the configuration is very convenient; you can directly call the corresponding configuration through `.` after instantiation. For example, to control the port the program listens on, the default value of `port` in `config.py` is `8001`, then you can directly use `app_config.port` after instantiating an `app_config`.

To change the running port, you can redefine the `PORT` environment variable in the `.envs`. The case of `PORT` is insensitive, `Port`, `PORT`, and `port` are all valid.

## 5. Deploy and manage the project

```bash
# Generate unit file <project_name>.service
rye run unit 
# It is recommended to run the generated unit file at the --user level
# It can be placed in the following four locations
# /usr/lib/systemd/user: Lowest priority, will be overridden by higher priority units of the same name
# ~/.local/share/systemd/user
# /etc/systemd/user: Globally shared user units
# ~/.config/systemd/user: Highest priority

# In this example, I put it in ~/.config/systemd/user
mkdir -p ~/.config/systemd/user

systemctl --user daemon-reload
systemctl --user enable <project_name>.service
systemctl --user start <project_name>.service
systemctl --user status <project_name>.service
systemctl --user stop <project_name>.service
systemctl --user disable <project_name>.service
```

## 6. Log Rotation

Log rotation relies on the tool `logrotate`, please ensure it is installed on your system.

First, use `rye run rotate` to generate the log rotation configuration file. At the end of the generated file, you will see a crontab task for executing log rotation in user space.

```bash
0 0 * * * /usr/sbin/logrotate /home/.../fsapi-template.conf
```

Please edit with `crontab -e` and add the task you see.

# License
[DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE](./LICENSE)