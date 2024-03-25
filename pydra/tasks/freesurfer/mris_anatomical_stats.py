"""
MRISAnatomicalStats
===================

Computes a number of anatomical properties.

Examples
--------

>>> task = MRISAnatomicalStats(
...     subject_id="subjid",
...     hemisphere="lh",
...     annotation_file="lh.aparc.annot",
...     format_stdout_as_table=True,
... )
>>> task.cmdline
'mris_anatomical_stats -a lh.aparc.annot -b subjid lh white'

>>> task = MRISAnatomicalStats(
...     subject_id="subjid",
...     hemisphere="lh",
...     label_file="lh.cortex.label",
...     format_stdout_as_table=True,
... )
>>> task.cmdline
'mris_anatomical_stats -l lh.cortex.label -b subjid lh white'
"""

import attrs

import pydra

from . import specs

__all__ = ["MRISAnatomicalStats"]


@attrs.define(slots=False, kw_only=True)
class MRISAnatomicalStatsSpec(pydra.specs.ShellSpec):
    """Specifications for mris_anatomical_stats."""

    subject_id: str = attrs.field(
        metadata={
            "help_string": "subject to process",
            "mandatory": True,
            "argstr": "",
            "position": -3,
        }
    )

    hemisphere: str = attrs.field(
        metadata={
            "help_string": "left or right hemisphere",
            "mandatory": True,
            "argstr": "",
            "position": -2,
            "allowed_values": {"lh", "rh"},
        }
    )

    surface_name: str = attrs.field(
        default="white",
        metadata={
            "help_string": "surface name",
            "argstr": "",
            "position": -1,
        },
    )

    label_file: str = attrs.field(
        metadata={
            "help_string": "restrict computation to the specified label",
            "argstr": "-l",
        }
    )

    annotation_file: str = attrs.field(
        metadata={
            "help_string": "compute statistics for each annotation in this file",
            "argstr": "-a",
        }
    )

    format_stdout_as_table: bool = attrs.field(
        metadata={
            "help_string": "write to stdout in table format",
            "argstr": "-b",
        }
    )

    output_table_file: str = attrs.field(
        metadata={
            "help_string": "output stats file in table format",
            "argstr": "-f",
            "output_file_template": "{hemisphere}.{surface_name}.stats",
        }
    )

    output_log_file: str = attrs.field(
        metadata={
            "help_string": "output stats file in log format",
            "argstr": "-log",
            "output_file_template": "{hemisphere}.{surface_name}.log",
        }
    )

    output_colortable_file: str = attrs.field(
        metadata={
            "help_string": "write colortable for annotations",
            "argstr": "-c",
            "requires": {"annotation_file"},
        }
    )

    subjects_dir: str = attrs.field(
        metadata={
            "help_string": "subjects directory",
            "argstr": "-sdir",
        }
    )


class MRISAnatomicalStats(pydra.engine.ShellCommandTask):
    """Task definition for mris_anatomical_stats."""

    input_spec = pydra.specs.SpecInfo(
        name="MRISAnatomicalStatsInput",
        bases=(MRISAnatomicalStatsSpec,),
    )

    output_spec = pydra.specs.SpecInfo(
        name="MRISAnatomicalStatsOutput",
        bases=(specs.SubjectsDirOutSpec,),
    )

    executable = "mris_anatomical_stats"
