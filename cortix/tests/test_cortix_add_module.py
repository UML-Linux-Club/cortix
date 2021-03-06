#!/usr/bin/env python

from cortix.src.module import Module
from cortix.examples.dummy_module import DummyModule

from cortix.src.cortix_main import Cortix

def test_cortix_add_module():
    # Init the Cortix object
    c = Cortix()

    num_modules = 100
    module_list = list()

    # Add 100 modules to the Cortix object
    for i in range(num_modules):
        # Initialize the module
        m = DummyModule()
        c.add_module(m)

        # Get ports
        p1 = m.get_port('test1-{}'.format(i))
        p2 = m.get_port('test2-{}'.format(i))

    # Make sure we have the correct modules
    assert len(c.modules) == num_modules
    for mod in c.modules:
        assert isinstance(mod, Module)
        assert len(mod.ports) == 2

if __name__ == "__main__":
    test_cortix_add_module()
