""" Check the rules
"""

import os
import pkg_resources
import yaml
import seabird

def load_rules():
    """ Try to read all rules with yaml

        https://github.com/castelao/seabird/issues/7
    """
    rules_dir = 'rules'
    rule_files = pkg_resources.resource_listdir(seabird.__name__, rules_dir)
    for rule_file in rule_files:
        print "loading rule: %s", (rule_file)
        text = pkg_resources.resource_string(seabird.__name__,
                os.path.join(rules_dir, rule_file))
        rule = yaml.load(text)
        assert type(rule) == dict
        assert len(rule.keys()) > 0

def test_answer():
    assert load_rules() == None
