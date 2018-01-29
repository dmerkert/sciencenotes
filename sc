#!/usr/bin/env python

import argument_parser
import config

parsed_args = argument_parser.parse()


cfg = config.Config()
if hasattr(parsed_args, 'config') and not parsed_args.config is None:
    cfg.parseConfig(file=parsed_args.config)
else:
    cfg.parseConfig()

argument_parser.callAction(parsed_args)
