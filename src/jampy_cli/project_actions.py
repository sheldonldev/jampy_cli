import shutil
from pathlib import Path
from typing import Annotated, Optional

import inflection
import toml
import typer
from rich import print
from util_common.datetime import format_now
from util_common.path import get_absolute_cwd_path, normalize_path

from .config import Config
from .notifier import Notifier


def create_default_project(
    name: str,
    project_dir: Path,
) -> None:
    def modify_toml():
        toml_str = project_dir.joinpath("pyproject.toml").read_text()
        toml_cfg = toml.loads(toml_str)
        toml_cfg["project"]["name"] = name
        toml_cfg["project"]["scripts"] = {"run": f"{name}.main:main"}
        toml_cfg["tool"]["setuptools"]["packages"]["find"]["include"] = [
            f"{name}*"
        ]
        project_dir.joinpath("pyproject.toml").write_text(toml.dumps(toml_cfg))

    def modify_cfg():
        code_str = project_dir.joinpath("src/name/_cfg.py").read_text()
        code_lines = code_str.splitlines()
        for i, line in enumerate(code_lines):
            if line.startswith("APP_NAME"):
                code_lines[i] = f'APP_NAME = "{name}"'

    def modify_cfg_test():
        code_str = project_dir.joinpath("tests/test_cfg.py").read_text()
        code_lines = code_str.splitlines()
        for i, line in enumerate(code_lines):
            if line.startswith("from temp_project"):
                code_lines[i] = line.replace('temp_project', name)

    def modify_log_test():
        code_str = project_dir.joinpath("tests/test_log.py").read_text()
        code_lines = code_str.splitlines()
        for i, line in enumerate(code_lines):
            if line.startswith("from temp_project"):
                code_lines[i] = line.replace('temp_project', name)

    template_dir = Config.STUBS_ROOT.joinpath("template-project-default")
    shutil.copytree(template_dir, project_dir)
    modify_toml()
    modify_cfg()
    modify_cfg_test()
    modify_log_test()
    shutil.move(project_dir / "src" / "name", project_dir / "src" / name)


def update_vscode_settings(dst_path: Path):
    template_dir = Config.STUBS_ROOT.joinpath("template-project-default")
    src_path = template_dir.joinpath(".vscode/settings.json")

    # backup th old
    shutil.copyfile(
        dst_path,
        dst_path.parent.joinpath(
            f"{dst_path.stem}_back{format_now()}{dst_path.suffix}"
        ),
    )
    shutil.copyfile(src_path, dst_path)


app = typer.Typer()


@app.command("c", help="Alias for create")
@app.command("create")
def create(
    project_path: Annotated[
        str,
        typer.Option("--path", "-p", help="Path to project root."),
    ],
    project_type: Annotated[
        Optional[str],
        typer.Option("--type", "-t", help="Type of project"),
    ] = None,
):
    """Create project."""

    name, project_dir = normalize_path(
        project_path, name_process_fn=lambda x: inflection.underscore(x.strip())
    )

    if project_dir.exists():
        Notifier.exists(print, str(project_dir))
        Notifier.exited(print)
        return

    if project_type is None:
        create_default_project(name, project_dir)
        Notifier.create_success(print, str(project_dir))
        Notifier.exited(print)
    else:
        # TODO
        Notifier.exited(print)


@app.command("ss", help="Alias for sync-settings")
@app.command("sync-settings")
def sync_settings(
    project_path: Annotated[
        Optional[str],
        typer.Option("--path", "-p", help="Path to project root."),
    ] = None
):
    """Sync vscode settings to the latest template."""
    if project_path is None:
        setting_path = ".vscode/settings.json"
    else:
        name, project_dir = normalize_path(project_path)
        # TODO:
        pass
    dst_path = get_absolute_cwd_path().joinpath(setting_path)
    if not dst_path.exists():
        Notifier.not_exists(print, str(dst_path))
        Notifier.exited(print)
    else:
        update_vscode_settings(dst_path)
        Notifier.update_success(print, str(dst_path))
        Notifier.exited(print)
