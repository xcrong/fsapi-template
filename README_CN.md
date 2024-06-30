![](https://codecov.io/github/xcrong/fsapi-template/branch/main/graph/badge.svg?token=tkq655ROg3)

# FastAPI 项目模板

一个 FastAPI 项目的模板仓库，可以自动生成 Unit 文件，方便用 Systemd 来启动、重启、停止项目。

# 如何食用？

## 1. 安装 rye

rye 作为项目管理工具，是必须的。你甚至可以不用安装 Python，但你得有 rye。

rye 不仅会进行自管理，还能为你管理项目需要用到的 Python 解释器。

本文默认项目开发和部署的环境都是 Linux。 在 Linux 上安装 rye 非常简单： `curl -sSf https://rye.astral.sh/get | bash`。

更多 rye 安装相关文档参见： [https://rye.astral.sh/guide/installation/#installing-rye](https://rye.astral.sh/guide/installation/#installing-rye)。


> 在 Windows 上依然可以使用本模板进行开发， 安装 rye 参见官网。本文档中的所有说明，除了 Unit 文件 相关的部分，均适用于 Windows 环境。

## 2. 克隆项目到本地

```bash
cd ~
git clone https://github.com/xcrong/fsapi-template.git <project_name> # 替换成你想要的项目名
cd <project_name> 
```


## 3. 同步环境

```bash
# 建立环境
# 在生产环境中，可以在所有的 sync 后面添加 --no-dev
# 以减少安装非必要依赖
rye sync 
# 使用你自己的信息初始化项目
rye run init
# 重新编译项目脚本
rye sync 
```

## 4. 进行项目开发

```bash
# 开发时，试试热更新项目，默认监视所有 *.py 文件和 .envs 文件
rye run dev 
# 启动项目
rye run start 
```

在项目开发的过程中，所有可配置项都建议放在环境变量中，即 `.envs` 文件中（请把 `.envs.example` 复制为 `.envs`）。

这些环境变量建议分为两组，一组用于控制程序的行为，一组用于控制 `uvicorn` 的行为。

首先在 `config.py` 的`AppConfig` 和 `UnicornConfig`中定义所需的环境变量，可以给出一个默认值。如果需要更改默认值，或者没有设置默认值，则需要在 `.envs` 中定义。


使用配置非常方便，可以在实例化后，直接通过 `.` 调用对应配置。比如控制程序监听的端口，`config.py` 中默认赋值 `port` 为`8001` ，然后实例化了一个 `app_config`，直接使用 `app_config.port` 即可。

若要更改运行端口，可以在 `.envs` 中重新定义 `PORT` 环境变量， `PORT`大小写不敏感，`Port` `PORT` `port` 都有效。


## 5. 部署项目与管理

```bash
# 生成单元文件 <project_name>.service
# 放在 cache 文件夹
rye run unit 
# 如果用 rye run unit <name>
# 可以指定生成 <name>.service
# 这在需要多个单元服务时格外有用
# 比如 rye run unit proxy
#      rye run unit spider


# 对于生成的单元文件建议在 --user 级别运行
# 可以放在下列四个位置
# /usr/lib/systemd/user：优先级最低，会被高优先级的同名 unit 覆盖
# ~/.local/share/systemd/user
# /etc/systemd/user：全局共享的用户级 unit[s]
# ~/.config/systemd/user：优先级最高

# 我这里示例放在 ~/.config/systemd/user
mkdir -p ~/.config/systemd/user

systemctl --user daemon-reload
systemctl --user enable <project_name>.service
systemctl --user start <project_name>.service
systemctl --user status <project_name>.service
systemctl --user stop <project_name>.service
systemctl --user disable <project_name>.service
```

> 注意：
> `systemctl --user` 启动的服务会在用户结束会话（比如退出 VPS ）时自动停止；要保持运行，需要启用 **linger**, 可以执行  `loginctl enable-linger $USER`。(可能需要 root 权限)
>
> 如果成功开启，执行 `loginctl show-user $USER | grep Linger` 会看到: 
> 
> ```shell
> $ loginctl show-user $USER | grep Linger
>  Linger=yes
> ```
>
> 如果你想了解更多，参见： 
>   - https://docs.oracle.com/en/operating-systems/oracle-linux/8/obe-systemd-linger/#enable-processes-to-continue-b
>   - https://wiki.archlinux.org/title/Systemd/User#Automatic_start-up_of_systemd_user_instances

## 6. 日志轮换

日志轮换依赖 `logrotate` 这个工具，请保证你的系统已经安装。

首先用 `rye run rotate` 生成日志轮换配置文件，在生成的末尾，你会看到一个 crontab 任务，用于在用户空间执行日志轮换。

生成日志轮换文件，也可以指定生成的文件名： `rye run rotate <name>` 将生成 `name.conf`。

```bash
0 0 * * * /usr/sbin/logrotate /home/.../fsapi-template.conf
```

请用 crontab -e 编辑， 把你看到的任务添加进行。

## 7. 其它
在 git push 之前，最好执行一下 `rye lint && rye fmt` 对代码中不符合规范的地方进行改进并格式化。

# License
[DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE](./LICENSE)
