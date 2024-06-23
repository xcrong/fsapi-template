import configparser
import os
import warnings
from typing import Any

import toml
from pydantic import BaseModel


class GitConfig(BaseModel):
    name: str
    email: str


def get_git_config() -> GitConfig:
    # 获取用户主目录
    home_dir = os.path.expanduser("~")
    gitconfig_path = os.path.join(home_dir, ".gitconfig")

    # 创建配置解析器
    config = configparser.ConfigParser()

    # 读取 .gitconfig 文件
    config.read(gitconfig_path)

    # 获取 user 部分的 name 和 email
    git_name = config.get("user", "name", fallback="")
    git_email = config.get("user", "email", fallback="")

    return GitConfig(name=git_name, email=git_email)


# 递归函数替换 JSON 数据中的特定字符串
def replace_values(obj, old_value, new_value):
    if isinstance(obj, dict):
        return {
            k: replace_values(v, old_value, new_value) for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [replace_values(i, old_value, new_value) for i in obj]
    elif isinstance(obj, str):
        return obj.replace(old_value, new_value)
    else:
        return obj


def reinit_git_repo():
    os.system("rm -rf .git")
    os.system("git init")
    os.system("git branch -m main")
    os.system("git add .")
    os.system('git commit -m "init"')


def init_project_details():
    # mk cache dir for log, *.conf, *.service
    pwd: str = os.getcwd()
    os.makedirs(os.path.join(pwd, "cache"), exist_ok=True)

    project_file = "pyproject.toml"
    with open(project_file, encoding="utf8") as f:
        pyproject = toml.load(f)

    pj_description = pyproject["project"]["description"]

    parent_dir_name = os.path.basename(os.getcwd())
    old_name = pyproject["project"]["name"]
    new_name = input(f"Project Name (Default: {parent_dir_name}): ").strip()
    if new_name == "":
        new_name = parent_dir_name
    pyproject: dict[str, Any] = replace_values(
        pyproject, old_name.replace("-", "_"), new_name
    )  # type: ignore
    pyproject: dict[str, Any] = replace_values(
        pyproject, old_name.replace("_", "-"), new_name
    )  # type: ignore

    # rename src/old_name to src/new_name
    os.rename(
        os.path.join("src", old_name.replace("-", "_")),
        os.path.join("src", new_name.replace("-", "_")),
    )

    # substitute old_name to new_name in src/new_name/__main__.py
    with open(
        os.path.join("src", new_name.replace("-", "_"), "__main__.py"),
        encoding="utf8",
    ) as f:
        content = f.read()
    content = content.replace(
        old_name.replace("-", "_"), new_name.replace("-", "_")
    )
    with open(
        os.path.join("src", new_name.replace("-", "_"), "__main__.py"),
        "w",
        encoding="utf8",
    ) as f:
        f.write(content)

    description = input(
        f"Descripte Your Project (Defaule: {pj_description}): "
    ).strip()
    if description != "":
        pyproject["project"]["description"] = description

    git_name, git_email = (get_git_config().name, get_git_config().email)
    author_name = input(f"Your name (Default: {git_name}: )").strip()
    if author_name == "":
        author_name = git_name

    author_email = input(f"Your email: (Defaule: {git_email}: )").strip()
    if author_email == "":
        author_email = git_email

    pyproject["project"]["authors"][0]["name"] = author_name
    pyproject["project"]["authors"][0]["email"] = author_email

    try:
        with open(project_file, "w", encoding="utf8") as f:
            toml.dump(pyproject, f)
    except Exception as e:
        warnings.warn(str(e), stacklevel=2)

    try:
        reinit_git_repo()
    except Exception as e:
        warnings.warn(str(e), stacklevel=2)
