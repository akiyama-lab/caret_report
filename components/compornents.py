#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from caret_analyze import Architecture

architecture_path = os.getenv(
    "ARCHITECTURE_FILE_PATH", "/home/akilab/autoware_analysis/architecture.yaml"
)

arch = Architecture(
    "lttng", "/home/akilab/caret_report/measurement/session-20250716133243"
)
# arch = Architecture("yaml", architecture_path)

arch.export("architecture.yaml")

with open("nodes.txt", "w") as a_file:
    for node in arch.node_names:
        a_file.write(f"{node}\n")
        # print(node)

with open("callbacks.txt", "w") as a_file:
    for callback in arch.callbacks:
        a_file.write(f"{callback.callback_name}\n")
        # print(callback.callback_name)

with open("topics.txt", "w") as a_file:
    for topic in arch.topic_names:
        a_file.write(f"{topic}\n")
        # print(topic)
