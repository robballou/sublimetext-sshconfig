#!/usr/bin/env python

from __future__ import annotations
import json
import re
import yaml

from typing import Callable, Literal, NotRequired, TypedDict
from yaml.representer import SafeRepresenter

SYNTAX_STEM = 'Packages/SSH Config/syntax/'
TEST_STEM = '../test/generated/syntax_test_'
SUPPORT_STEM = '../support/generated/'


class CompletionMetadata(TypedDict):
    scope: str
    kind: list[str]
    annotation: str


class CompletionItem(TypedDict):
    kind: list[str] | Literal['snippet']
    annotation: str
    trigger: str
    contents: str
    details: NotRequired[str]


class CompletionFillins(TypedDict):
    details: str
    values: str | list[str]


class CompletionSet(TypedDict):
    completions: CompletionMetadata
    items: dict[str,CompletionFillins]


class CompletionYaml(TypedDict):
    scope: str
    completions: list[CompletionItem]


class CryptoFillins(TypedDict):
    scope: str
    items: list[str]


class CryptoSet(TypedDict):
    completions: CompletionMetadata
    active: CryptoFillins
    deprecated: CryptoFillins


class SyntaxContext(TypedDict):
    include: NotRequired[str]
    match: NotRequired[str]
    scope: NotRequired[str]
    captures: NotRequired[dict[int,str]]
    pop: NotRequired[bool | int]
    push: NotRequired[str | list[str] | list[SyntaxContext]]


class SyntaxYaml(TypedDict):
    scope: str
    name: NotRequired[str]
    hidden: NotRequired[bool]
    file_extensions: NotRequired[list[str]]
    hidden_file_extensions: NotRequired[list[str]]
    extends: NotRequired[str | list[str]]
    version: NotRequired[int]
    variables: NotRequired[dict[str, str]]
    contexts: dict[str, list[SyntaxContext]]


def build_ssh_options():
    with open('options.yaml', 'r') as stream:
        ssh_options_input: dict[str, CompletionSet] = yaml.load(  # pyright: ignore[reportAssignmentType]
            stream, Loader=yaml.BaseLoader)

    for domain, settings in ssh_options_input.items():
        completions_yaml: CompletionYaml = {
            'scope': settings['completions']['scope'],
            'completions': [],
        }
        completions: list[CompletionItem] = []
        snippet_spacer: str = settings['completions'].get('snippet_spacer', ' ')
        default_kind: list[str] = settings['completions']['kind']
        annotation: str = settings['completions']['annotation']

        for keyword, options in settings['items'].items():
            details: str = options.get('details', '') if options else ''
            _ = completions.append({
                'trigger': keyword,
                'contents': keyword,
                'annotation': annotation,
                'kind': default_kind,
                'details': details,
            })
            if not options or 'values' not in options:
                continue

            values: str | list[str] = options['values']
            if isinstance(values, (list)):
                v_gen = (v.replace('}', '\\}').replace('$', '\\$')
                         for v in values)
                value_string = f'${{0:{{ {" | ".join(v_gen)} \\}}}}'
            elif '$' not in values:
                value_string = f'${{0:{values}}}'
            else:
                value_string = values

            _ = completions.append({
                'trigger': keyword.lower(),
                'contents': f'{keyword}{snippet_spacer}{value_string}',
                'annotation': annotation,
                'kind': 'snippet',
                'details': details,
            })

        completions_yaml['completions'] = completions

        with open(f'{SUPPORT_STEM}{domain}.sublime-completions', 'w') as f:
            json.dump(completions_yaml, f, indent=4)


def build_ssh_option_test():
    with open('options.yaml', 'r') as stream:
        ssh_options_input: dict[str, CompletionSet] = yaml.load(  # pyright: ignore[reportAssignmentType]
            stream, Loader=yaml.BaseLoader)

    test_content = [
        f'# SYNTAX TEST "{SYNTAX_STEM}SSH Config.sublime-syntax"\n',
        'Host example.com\n',
    ]

    for item, content in ssh_options_input['SSH Config']['items'].items():
        if 'values' not in content:
            continue
        if '$' in content['values']:
            continue

        key_scope = 'meta.mapping.key keyword.other'
        if item in {'Hostname'}:
            key_scope = 'meta.mapping.key keyword.declaration'

        value_list = content['values']
        if isinstance(value_list, str):
            value_list = [value_list]

        for value in value_list:
            if value in {'...'}:
                continue

            val_scope = 'meta.mapping.value - invalid'
            if value in {'md5'}:
                val_scope = 'meta.mapping.value - invalid.illegal'

            test_content.append(f' {item} {value}')
            test_content.append(
                f'#{"^" * len(item)} {key_scope}')
            test_content.append(
                f'#{" " * len(item)} {"^" * len(value)} {val_scope}')

    with open(f'{TEST_STEM}client_options.ssh_config', 'w') as test_file:
        _ = test_file.write('\n'.join(test_content))


def build_sshd_index_test():
    with open('options.yaml', 'r') as stream:
        ssh_options_input: dict[str, CompletionSet] = yaml.load(  # pyright: ignore[reportAssignmentType]
            stream, Loader=yaml.BaseLoader)

    test_content = [
        f'# SYNTAX TEST "{SYNTAX_STEM}SSHD Config.sublime-syntax"\n',
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

    with open(f'{TEST_STEM}server_index.sshd_config', 'w') as test_file:
        _ = test_file.write('\n'.join(test_content))


def build_crypto():

    # Set up YAML dump style
    class literal_str(str): pass

    def change_style(style: Literal['"', '|', '>'],
                     representer: Callable['...', yaml.ScalarNode]):
        def new_representer(dumper: yaml.Dumper, data: str) -> yaml.ScalarNode:
            scalar = representer(dumper, data)
            scalar.style = style
            return scalar
        return new_representer

    represent_literal_str = change_style('|', SafeRepresenter.represent_str)
    yaml.add_representer(literal_str, represent_literal_str)

    # Process
    with open('crypto.yaml', 'r') as stream:
        crypto_input: dict[str, CryptoSet] = yaml.load(  # pyright: ignore[reportAssignmentType]
            stream, Loader=yaml.BaseLoader)

    test_content: list[str] = [
        f'# SYNTAX TEST "{SYNTAX_STEM}SSH Crypto.sublime-syntax"\n',
    ]
    syntax_content: SyntaxYaml = {
        'name': 'SSH Crypto',
        'hidden': True,
        'scope': 'text.ssh.crypto',
        'extends': 'SSH Common.sublime-syntax',
        'version': 2,
        'hidden_file_extensions': [
            'syntax_test_crypto',
        ],
        'contexts': {},
        'variables': {},
    }
    syntax_contexts: dict[str, list[SyntaxContext]] = {
        'main': [
            {'include': 'comments'},
        ],
    }
    syntax_variables: dict[str, str] = {}

    for domain, settings in crypto_input.items():
        completions_yaml: CompletionYaml = {
            'scope': settings['completions']['scope'].strip(),
            'completions': [],
        }
        completions: list[CompletionItem] = []
        default_kind: list[str] = settings['completions']['kind']
        annotation: str = settings['completions']['annotation']
        active_scope: str = settings['active']['scope']
        deprec_scope: str = settings['deprecated']['scope']

        domain_ = domain.replace('-', '_')

        test_content.append(f'\n###[ {domain + " ]":#<74}\n')
        _ = syntax_contexts['main'].append({
            'match': fr'^{annotation}:',
            'push': [
                {'include': 'pop-before-nl'},
                {'include': f'ssh-{domain}'}
            ]
        })
        syntax_contexts[f'ssh-{domain}'] = [
            {
                'match': fr'\b{{{{{domain_}_active}}}}(?=[,\s\"])',
                'scope': active_scope,
            },
            {
                'match': fr'\b{{{{{domain_}_deprec}}}}(?=[,\s\"])',
                'scope': deprec_scope,
            },
        ]
        syntax_variables[f'{domain_}_active'] = literal_str(
            fr"""(?x:{'\n  '}{'\n| '.join(
                re.escape(i) for i in
                sorted(settings['active']['items'], reverse=True)
            )}{'\n'})"""
        )
        syntax_variables[f'{domain_}_deprec'] = literal_str(
            fr"""(?x:{'\n  '}{'\n| '.join(
                re.escape(i) for i in
                sorted(settings['deprecated']['items'], reverse=True)
            )}{'\n'})"""
        )

        for item in settings['active']['items']:
            _ = completions.append({
                'trigger': item,
                'contents': item,
                'annotation': annotation,
                'kind': default_kind,
            })
            test_content.append(f'{annotation}: {item}')
            test_content.append(
                f'#{" " * len(annotation)} {"^" * len(item)} {active_scope}')

        for item in settings['deprecated']['items']:
            _ = completions.append({
                'trigger': item,
                'contents': item,
                'annotation': f'deprecated {annotation}',
                'kind': default_kind,
                'details': 'Deprecated',
            })
            test_content.append(f'{annotation}: {item}')
            test_content.append(
                f'#{" " * len(annotation)} {"^" * len(item)} {deprec_scope}')

        completions_yaml['completions'] = completions

        with open(f'{SUPPORT_STEM}{domain}.sublime-completions', 'w') as f:
            json.dump(completions_yaml, f, indent=4)

    syntax_content['contexts'] = syntax_contexts
    syntax_content['variables'] = syntax_variables

    with open('../syntax/SSH Crypto.sublime-syntax', 'w') as syntax_file:
        _ = syntax_file.write('%YAML 1.2\n---\n')
        _ = yaml.dump(syntax_content, syntax_file)

    with open(f'{TEST_STEM}crypto', 'w') as test_file:
        _ = test_file.write('\n'.join(test_content))


def main():
    build_ssh_options()
    build_ssh_option_test()
    build_sshd_index_test()
    build_crypto()


if __name__ == '__main__':
    main()
