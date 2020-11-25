"""Utility functions."""
from collections import defaultdict
from typing import Any, Dict
from xml.etree.ElementTree import Element


def etree_to_dict(t: Element) -> Dict[str, Any]:
    """Convert XML element tree to dictionary.

    Args:
        tree (Element): XML Input

    Returns:
        Dict[str, Any]: Converted dictionary output
    """
    d: Dict[str, Any] = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.text:
        text = t.text.strip()
        if not (children or t.attrib):
            d[t.tag] = text
    return d
