"""
Small utility to take pytest-benchmark results and update our README.md with
them.
"""
import sys
import json

from humanmark import Fragment, load, HTMLBlock, Header, Text, Paragraph, dump


def main(argv):
    with open('benchmark.json') as src:
        j = json.load(src)

    groups = {}
    for benchmark in j['benchmarks']:
        groups.setdefault(benchmark['group'], []).append({
            'name': benchmark['name'],
            'min': benchmark['stats']['min'],
            'max': benchmark['stats']['max'],
            'mean': benchmark['stats']['mean']
        })

    readme_summaries = Fragment()
    for group_name, result in groups.items():
        result.sort(key=lambda v: v['min'])

        readme_summaries.extend((
            Header(3, children=[Text(group_name)]),
            Paragraph(children=[
                Text('| library | min (ms) | max (ms) | mean (ms) |\n'),
                Text('| ------- | -------- | -------- | --------- |\n'),
                *(
                    Text(
                        f'| {v["name"]} | {v["min"] * 1000:.4f} '
                        f'| {v["max"] * 1000:.4f} '
                        f'| {v["mean"] * 1000:.4f} '
                        f'|\n'
                    )
                    for v in result
                )
            ])
        ))

    with open('README.md') as src:
        readme = load(src)

    start = readme.find_one(
        HTMLBlock,
        f=lambda block: block.content == (
            '<!-- start_performance_block -->\n'
        )
    )

    end = readme.find_one(
        HTMLBlock,
        f=lambda block: block.content == '<!-- end_performance_block -->\n'
    )

    # Erase all the content between the open and closing blocks.
    node = start.next
    while node:
        if node == end:
            break

        node = node.delete()

    start.append_sibling(readme_summaries)

    with open('README.md', 'w') as out:
        dump(readme, out)


if __name__ == '__main__':
    sys.exit(main(sys.argv))