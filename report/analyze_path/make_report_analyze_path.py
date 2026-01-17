# Copyright 2022 Tier IV, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Script to make report page
"""
import glob
import argparse
from pathlib import Path
import sys
import yaml
import flask
import os


app = flask.Flask(__name__)


def render_page(stats, title, sub_title, destination_path, template_path,
                message_flow_start=None, message_flow_end=None,
                message_flow_trigger=None, message_flow_margin_s=None):
    """Render html page"""
    with app.app_context():
        with open(template_path, 'r', encoding='utf-8') as f_html:
            template_string = f_html.read()
            rendered = flask.render_template_string(
                template_string,
                title=title,
                sub_title=sub_title,
                stats=stats,
                message_flow_start=message_flow_start,
                message_flow_end=message_flow_end,
                message_flow_trigger=message_flow_trigger,
                message_flow_margin_s=message_flow_margin_s,
            )

        with open(destination_path, 'w', encoding='utf-8') as f_html:
            f_html.write(rendered)


def make_report(stats_path: str):
    """Make report page"""
    stats = None
    with open(stats_path, 'r', encoding='utf-8') as f_yaml:
        stats = yaml.safe_load(f_yaml)

    # Get message flow parameters from environment
    message_flow_start = os.environ.get('message_flow_start')
    message_flow_end = os.environ.get('message_flow_end')
    message_flow_trigger = os.environ.get('message_flow_trigger')
    message_flow_margin_s = os.environ.get('message_flow_margin_s')

    # Convert empty strings to None
    message_flow_start = int(message_flow_start) if message_flow_start and message_flow_start != '0' else None
    message_flow_end = int(message_flow_end) if message_flow_end and message_flow_end != '0' else None
    message_flow_trigger = int(message_flow_trigger) if message_flow_trigger else None
    message_flow_margin_s = float(message_flow_margin_s) if message_flow_margin_s else None

    stats_dir = Path(stats_path).resolve().parent
    destination_path = f'{stats_dir}/index.html'
    template_path = f'{Path(__file__).resolve().parent}/template_path_index.html'
    title = 'Path List'
    sub_title = stats_path.split('/')[-3]
    render_page(stats, title, sub_title, destination_path, template_path)

    for path_info in stats:
        target_path_name = path_info['target_path_name']
        destination_path = f'{stats_dir}/{target_path_name}.html'
        template_path = f'{Path(__file__).resolve().parent}/template_path_detail.html'
        title = f'Path: {target_path_name}'
        sub_title = stats_path.split('/')[-3]
        render_page(path_info, title, sub_title, destination_path, template_path,
                   message_flow_start=message_flow_start,
                   message_flow_end=message_flow_end,
                   message_flow_trigger=message_flow_trigger,
                   message_flow_margin_s=message_flow_margin_s)


def parse_arg():
    """Parse arguments"""
    parser = argparse.ArgumentParser(
                description='Script to make report page')
    parser.add_argument('dest_dir', nargs=1, type=str)
    args = parser.parse_args()
    return args


def main():
    """main function"""
    args = parse_arg()

    dest_dir = args.dest_dir[0]
    stats_path_list = glob.glob(f'{dest_dir}/analyze_path/**/stats_path.yaml', recursive=True)

    if not stats_path_list:
        print('Warning. No stats file exists.', file=sys.stderr)
    else:
        for stats_path in stats_path_list:
            make_report(stats_path)
        print('<<< OK. report_analyze_path is created >>>')


if __name__ == '__main__':
    main()
