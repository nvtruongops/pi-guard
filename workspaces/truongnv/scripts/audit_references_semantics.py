#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Forwarding stub to unified audit_workspace.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from audit_workspace import run_semantics_audit
if __name__ == "__main__":
    sys.exit(run_semantics_audit())
