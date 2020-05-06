#!/usr/bin/env python

import json
import os
import sys
import yaml


def build_ssh_options():
    with open('options.yaml', 'r') as stream:
        ssh_options_input = yaml.load(stream, Loader=yaml.BaseLoader)

    for domain, settings in ssh_options_input.items():
        completions = {
            'scope': settings['completions']['scope'],
            'completions': [],
        }
        snippet_spacer = settings['completions'].get('snippet_spacer', ' ')
        default_kind = settings['completions']['kind']
        annotation = settings['completions']['annotation']

        for keyword, options in settings['items'].items():
            details = options.get('details', '') if options else ''
            completions['completions'].append({
                'trigger': keyword,
                'contents': keyword,
                # 'annotation': annotation,
                'kind': default_kind,
                'details': details,
            })
            if not options or 'values' not in options:
                continue

            values = options['values']
            if isinstance(values, (str)):
                value_string = values
            else:
                value_string = f'${{0:{{ {" | ".join(values)} \\}}}}'
            completions['completions'].append({
                'trigger': keyword.lower(),
                'contents': f'{keyword}{snippet_spacer}{value_string}',
                # 'annotation': annotation,
                'kind': 'snippet',
                'details': details,
            })

        with open(f'../Support/{domain}.sublime-completions', 'w') as f:
            json.dump(completions, f, indent=4)


def build_crypto():
    with open('crypto.yaml', 'r') as stream:
        crypto_input = yaml.load(stream, Loader=yaml.BaseLoader)

    for domain, settings in crypto_input.items():
        completions = {
            'scope': settings['completions']['scope'],
            'completions': [],
        }
        default_kind = settings['completions']['kind']
        annotation = settings['completions']['annotation']

        for item in settings['active']['items']:
            completions['completions'].append({
                'trigger': item,
                'contents': item,
                'annotation': annotation,
                'kind': default_kind,
            })

        for item in settings['deprecated']['items']:
            completions['completions'].append({
                'trigger': item,
                'contents': item,
                'annotation': f'deprecated {annotation}',
                'kind': default_kind,
                'details': 'Deprecated',
            })

        with open(f'../Support/{domain}.sublime-completions', 'w') as f:
            json.dump(completions, f, indent=4)


def main():
    build_ssh_options()
    build_crypto()


if __name__ == '__main__':
    main()
