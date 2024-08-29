# You shouldn't change  name of function or their arguments
# but you can change content of the initial functions.
from argparse import ArgumentParser
from typing import List, Optional, Sequence
import requests
import xml.etree.ElementTree as ET
import json


class UnhandledException(Exception):
    pass


def rss_parser(
    xml: str,
    limit: Optional[int] = None,
    json: bool = False,
) -> List[str]:
    """
    RSS parser.

    Args:
        xml: XML document as a string.
        limit: Number of the news to return. if None, returns all news.
        json: If True, format output as JSON.

    Returns:
        List of strings.
        Which then can be printed to stdout or written to file as a separate lines.

    Examples:
        >>> xml = '<rss><channel><title>Some RSS Channel</title><link>https://some.rss.com</link><description>Some RSS Channel</description></channel></rss>'
        >>> rss_parser(xml)
        ["Feed: Some RSS Channel",
        "Link: https://some.rss.com"]
        >>> print("\\n".join(rss_parser(xmls)))
        Feed: Some RSS Channel
        Link: https://some.rss.com
    """

    # Your code goes here
    root = ET.fromstring(xml)

    channel = root.findall('channel')[0]

    # CLI output standart
    tree = create_root_tree(channel, item_size=limit)

    cli_output = get_cli_output(tree)

    # CLI output json
    tree_json_cli = parse_as_json(tree)

    return tree_json_cli if json else cli_output


def parse_as_json(tree):
    json_tree = json.dumps(tree, indent=2)
    json_lines = json_tree.splitlines()

    return json_lines


def get_cli_output(tree, is_item=False):
    channel_output = {
        'title': 'Feed: ',
        'link': 'Link: ',
        'lastBuildDate': 'Last Build Date: ',
        'pubDate': 'Publish Date: ',
        'language': 'Language: ',
        'category': 'Categories: ',
        'managinEditor': 'Editor: ',
        'description': 'Description: ',
        'items': ''
    }
    item_output = {
        'title': 'Title: ',
        'author': 'Author: ',
        'pubDate': 'Published: ',
        'link': 'Link: ',
        'category': 'Categories: ',
        'description': '\n'
    }
    tree_cli = list()

    output = channel_output

    if is_item:
        output = item_output

    for tag in tree:
        if tag == 'items':
            for item in tree[tag]:
                # Add newline after each item
                tree_cli.append('')

                item = get_cli_output(item, True)
                # Add each item element string
                for el in item:
                    tree_cli.append(el)
            continue

        # Unpack categories
        elif tag == 'category':
            categories = list()
            if type(tree[tag]) is list:
                for category in tree[tag]:
                    categories.append(category)

            else:
                categories = tree[tag]

            tree[tag] = categories

        if type(tree[tag]) is list:
            tag_branch = f'{output[tag]}{", ".join(tree[tag])}'

        else:
            tag_branch = f'{output[tag]}{tree[tag]}'

        tree_cli.append(tag_branch)

    return tree_cli


def order_tree(tree, is_item=False):
    channel_order = {
        'title': '',
        'link': '',
        'lastBuildDate': '',
        'pubDate': '',
        'language': '',
        'category': '',
        'managinEditor': '',
        'description': '',
        'items': ''
    }
    item_order = {
        'title': '',
        'author': '',
        'pubDate': '',
        'link': '',
        'category': '',
        'description': ''
    }
    order = channel_order

    if is_item:
        order = item_order

    # Reorder item
    for tag, content in tree.items():
        if order.get(tag, None) is not None:
            order[tag] = content

    empty_tags = list()
    # Remove empty content
    for tag in order:
        if not order[tag]:
            empty_tags.append(tag)

    for tag in empty_tags:
        del order[tag]

    return order


def create_root_tree(root_item, item_size=None, is_item=False):
    tree_dict = dict()
    lst = list()
    for element in root_item:
        # Get item list
        if element.text is None:
            item_dict = create_root_tree(element, is_item=True)
            item_dict = order_tree(item_dict, is_item=True)
            if item_size:
                if len(lst) < item_size:
                    lst.append(item_dict)
                continue
            lst.append(item_dict)
            continue
        # Get items which have same key
        if tree_dict.get(element.tag, None) is not None:
            duplicate_key_lst = [tree_dict[element.tag]]
            duplicate_key_lst.append(element.text)

            tree_dict[element.tag] = duplicate_key_lst
            continue

        tree_dict[element.tag] = element.text

    # its full root tree
    # add items to tree_dict
    if lst:
        tree_dict['items'] = list()
        for item in lst:
            tree_dict['items'].append(item)

    if not is_item:
        tree_dict = order_tree(tree_dict)

    return tree_dict


def main(argv: Optional[Sequence] = None):
    """
    The main function of your task.
    """
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )
    args = parser.parse_args(argv)
    xml = requests.get(args.source).text
    try:
        print("\n".join(rss_parser(xml, args.limit, args.json)))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
