"""FMS ZIP import engine — see importer.py for the entry point.

Turns an FMS métier ZIP (référentiel, learning map, module map, blueprint,
modules, QCM, cas N2, assessments, templates, guides — one Markdown file
per artifact) into searchable, navigable `fms_resources` documents, with
an auto-generated sommaire and prerequisite graph per formation.
"""

from .importer import import_fms_zip
from .indexer import build_dependency_graph, build_navigation, search_resources
from .models import FmsResource, ImportIssue, ImportReport

__all__ = [
    "import_fms_zip",
    "build_navigation",
    "build_dependency_graph",
    "search_resources",
    "FmsResource",
    "ImportReport",
    "ImportIssue",
]
