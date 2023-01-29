#!/usr/bin/env python

""" Check the rules
"""

import os
import pkg_resources
import json
import re
import seabird


def test_load_available_rules():
    """Try to read all available rules

    https://github.com/castelao/seabird/issues/7
    """
    rules_dir = "rules"
    rule_files = pkg_resources.resource_listdir(seabird.__name__, rules_dir)
    rule_files = [f for f in rule_files if re.match("^(?!refnames).*json$", f)]
    for rule_file in rule_files:
        print("loading rule: %s", (rule_file))
        text = pkg_resources.resource_string(
            seabird.__name__, os.path.join(rules_dir, rule_file)
        )
        rule = json.loads(text.decode("utf-8"))
        assert type(rule) == dict
        assert len(rule.keys()) > 0
