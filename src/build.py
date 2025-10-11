#!/usr/bin/env python

from __future__ import annotations
import json
import re
import yaml

CompletionItem: dict[str, str | list[str]]
CompletionMetadata: dict[str, str | list[str]]
CompletionSet: dict[str, CompletionItem | CompletionMetadata]
CryptoSet: dict[str, str | list[str]]


def build_ssh_options():
    with open('options.yaml', 'r') as stream:
        ssh_options_input: dict[str, CompletionSet] = yaml.load(
            stream, Loader=yaml.BaseLoader)

    for domain, settings in ssh_options_input.items():
        completions: CompletionItem = {
            'scope': settings['completions']['scope'],
            'completions': [],
        }
        snippet_spacer: str = settings['completions'].get('snippet_spacer', ' ')
        default_kind: list[str] = settings['completions']['kind']
        annotation: str = settings['completions']['annotation']

        for keyword, options in settings['items'].items():
            details: str = options.get('details', '') if options else ''
            _ = completions['completions'].append({
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


def build_sshd_index_test():
    with open('options.yaml', 'r') as stream:
        ssh_options_input: dict[str, CompletionSet] = yaml.load(
            stream, Loader=yaml.BaseLoader)

    test_content = [
        '# SYNTAX TEST "Packages/SSH Config/SSHD Config.sublime-syntax"\n',
    ]

    for item in ssh_options_input['SSHD Config']['items']:
        if item in {'Match'}:
            continue

        test_content.append(f' {item} no')
        test_content.append(
            f'#{"@" * len(item)} local-definition')
        if item.endswith('Command'):
            test_content.append(
                f'#{" " * len(item)} @@ reference')
        test_content.append(f'#{item} no')
        test_content.append(
            f'#{"@" * len(item)} local-definition\n')

    with open('../Tests/syntax_test_server_index.sshd_config', 'w') as test_file:
        test_file.write('\n'.join(test_content))


def build_crypto():
    with open('crypto.yaml', 'r') as stream:
        crypto_input = yaml.load(stream, Loader=yaml.BaseLoader)

    test_content = [
        '# SYNTAX TEST "Packages/SSH Config/SSH Crypto.sublime-syntax"\n',
    ]
    syntax_content = {
        'name': 'SSH Crypto',
        'hidden': True,
        'scope': 'text.ssh.crypto',
        'extends': 'SSH Common.sublime-syntax',
        'version': 2,
        'hidden_file_extensions': [
            'syntax_test_crypto',
        ],
        'contexts': {
            'main': [
                {'include': 'comments'},
            ]
        }
    }

    for domain, settings in crypto_input.items():
        completions = {
            'scope': settings['completions']['scope'].strip(),
            'completions': [],
        }
        default_kind: list[str] = settings['completions']['kind']
        annotation: str = settings['completions']['annotation']
        active_scope: str = settings['active']['scope']
        deprec_scope: str = settings['deprecated']['scope']

        test_content.append(f'\n###[ {domain + " ]":#<74}\n')
        _ = syntax_content['contexts']['main'].append({
            'match': fr'^{annotation}:',
            'push': [
                {'include': 'pop-before-nl'},
                {'include': f'ssh-{domain}'}
            ]
        })
        syntax_content['contexts'][f'ssh-{domain}'] = [
            {
                'match': fr"""\b(?:{'|'.join(
                    re.escape(i) for i in
                    sorted(settings['active']['items'], reverse=True)
                )})(?=[,\s\"])""",
                'scope': active_scope,
            },
            {
                'match': fr"""\b(?:{'|'.join(
                    re.escape(i) for i in
                    sorted(settings['deprecated']['items'], reverse=True)
                )})(?=[,\s\"])""",
                'scope': deprec_scope,
            },
        ]

        for item in settings['active']['items']:
            _ = completions['completions'].append({
                'trigger': f'{item}\t{annotation}',
                'contents': item,
                'annotation': annotation,
                'kind': default_kind,
            })
            test_content.append(f'{annotation}: {item}')
            test_content.append(
                f'#{" " * len(annotation)} {"^" * len(item)} {active_scope}')

        for item in settings['deprecated']['items']:
            _ = completions['completions'].append({
                'trigger': f'{item}\tdeprecated {annotation}',
                'contents': item,
                'annotation': f'deprecated {annotation}',
                'kind': default_kind,
                'details': 'Deprecated',
            })
            test_content.append(f'{annotation}: {item}')
            test_content.append(
                f'#{" " * len(annotation)} {"^" * len(item)} {deprec_scope}')

        with open(f'../Support/{domain}.sublime-completions', 'w') as f:
            json.dump(completions, f, indent=4)

    with open('../SSH Crypto.sublime-syntax', 'w') as syntax_file:
        syntax_file.write('%YAML 1.2\n---\n')
        yaml.dump(syntax_content, syntax_file)

    with open('../Tests/syntax_test_crypto', 'w') as test_file:
        test_file.write('\n'.join(test_content))


def main():
    build_ssh_options()
    build_sshd_index_test()
    build_crypto()


if __name__ == '__main__':
    main()
