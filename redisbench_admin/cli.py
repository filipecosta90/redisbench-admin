import argparse
import sys

import toml

from redisbench_admin.compare.compare import create_compare_arguments, compare_command_logic
from redisbench_admin.export.export import create_export_arguments, export_command_logic
from redisbench_admin.run.run import create_run_arguments, run_command_logic


def populate_with_poetry_data():
    poetry_data = toml.load("pyproject.toml")['tool']['poetry']
    project_name = poetry_data["name"]
    project_version = poetry_data["version"]
    project_description = poetry_data["description"]
    return project_name, project_description, project_version


def main():
    tool = None
    if len(sys.argv) < 2:
        print(
            "A minimum of 2 arguments is required: redisbench-admin <tool> <arguments>. Use redisbench-admin --help if you need further assistance.")
        sys.exit(1)
    requested_tool = sys.argv[1]
    project_name, project_description, project_version = populate_with_poetry_data()
    parser = argparse.ArgumentParser(
        description=project_description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--version', default=False, action='store_true', help='print version and exit')
    if requested_tool == "run":
        parser = create_run_arguments(parser)
    elif requested_tool == "compare":
        parser = create_compare_arguments(parser)
    elif requested_tool == "export":
        parser = create_export_arguments(parser)
    elif requested_tool == "--version":
        print("{project_name} {project_version}".format(project_name=project_name, project_version=project_version))
        sys.exit(0)
    elif requested_tool == "--help":
        print("{project_name} {project_version}".format(project_name=project_name, project_version=project_version))
        print("usage: {project_name} <tool> <args>...".format(project_name=project_name))
        print(
            "\t-) To know more on how to run benchmarks: {project_name} run --help".format(project_name=project_name))
        print(
            "\t-) To know more on how to compare benchmark results: {project_name} compare --help".format(
                project_name=project_name))
        print(
            "\t-) To know more on how to export benchmark results: {project_name} export --help".format(
                project_name=project_name))
        sys.exit(0)
    else:
        print("Invalid redisbench-admin <tool>. Requested tool: {}. Available tools: [run,export,compare]".format(
            requested_tool))
        sys.exit(1)

    argv = sys.argv[2:]
    args = parser.parse_args(args=argv)
    if args.version:
        print("{project_name} {project_version}".format(project_name=project_name, project_version=project_version))
        sys.exit(0)

    if requested_tool == "run":
        run_command_logic(args)
    if requested_tool == "compare":
        export_command_logic(args)
    if requested_tool == "export":
        compare_command_logic(args)