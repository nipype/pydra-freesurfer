import os
import typing as ty

from pydra.engine.specs import ShellOutSpec, ShellSpec, SpecInfo

from pydra import ShellCommandTask

__all__ = ["MRIVol2Vol"]


class MRIVol2Vol(ShellCommandTask):
    """Task for mri_vol2vol.

    Resamples a volume into another field-of-view using various types of matrices (FreeSurfer, FSL, SPM, and MNI). This
    is meant to be used in conjunction with tkregister2.

    Examples
    --------

    1. Resample functional data into anatomical space:

    >>> task = MRIVol2Vol(
    ...     regfile="register.dat",
    ...     movvol="func.nii.gz",
    ...     fstarg=True,
    ...     outvol="func-in-anat.mgh",
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov func.nii.gz --o func-in-anat.mgh --reg register.dat --fstarg'

    2. Resample anatomical data into functional space:

    >>> task = MRIVol2Vol(
    ...     regfile="register.dat",
    ...     movvol="func.nii.gz",
    ...     fstarg=True,
    ...     outvol="anat-in-func.mgh",
    ...     invert=True,
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov func.nii.gz --o anat-in-func.mgh --reg register.dat --fstarg --inv'

    3. Map functional to anatomical without resampling:

    >>> task = MRIVol2Vol(
    ...     regfile="register.dat",
    ...     movvol="func.nii.gz",
    ...     fstarg=True,
    ...     outvol="func.new.vox2ras.nii.gz",
    ...     no_resample=True,
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov func.nii.gz --o func.new.vox2ras.nii.gz --reg register.dat --fstarg --no-resample'

    4. Map a binary mask in functional space to anatomical space:

    >>> task = MRIVol2Vol(
    ...     regfile="register.dat",
    ...     movvol="mask.nii.gz",
    ...     fstarg=True,
    ...     outvol="mask-in-anat.mgh",
    ...     interp="nearest",
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov mask.nii.gz --o mask-in-anat.mgh --reg register.dat --fstarg --interp nearest'

    5. Map functional data to talairach (MNI305) space with 2mm isotropic resolution:

    >>> task = MRIVol2Vol(
    ...     movvol="func.nii.gz",
    ...     outvol="func-in-tal.2mm.mgh",
    ...     regfile="register.dat",
    ...     talairach=True,
    ...     talairach_resolution=2,
    ... )
    >>> task.cmdline
    'mri_vol2vol --mov func.nii.gz --o func-in-tal.2mm.mgh --reg register.dat --tal --talres 2'
    """

    input_spec = SpecInfo(
        name="MRIVol2VolInput",
        fields=[
            (
                "movvol",
                str,
                {
                    "help_string": "input volume (or output template with --inv)",
                    "argstr": "--mov {movvol}",
                },
            ),
            (
                "outvol",
                str,
                {
                    "help_string": "output volume",
                    "argstr": "--o {outvol}",
                    "output_file_template": "{outvol}",
                },
            ),
            (
                "regfile",
                os.PathLike,
                {
                    "help_string": "registration matrix generated by FreeSurfer",
                    "argstr": "--reg {regfile}",
                },
            ),
            (
                "fslfile",
                os.PathLike,
                {
                    "help_string": "registration matrix generated by FSL flirt",
                    "argstr": "--fsl {fslfile}",
                },
            ),
            (
                "xfmfile",
                os.PathLike,
                {
                    "help_string": "MNI-style registration matrix",
                    "argstr": "--xfm {xfmfile}",
                },
            ),
            (
                "talairach",
                bool,
                {
                    "help_string": "resample moving volume to talairach",
                    "argstr": "--tal",
                },
            ),
            (
                "talairach_resolution",
                int,
                {
                    "help_string": "resoluton of the talairach template",
                    "argstr": "--talres {talairach_resolution}",
                    "allowed_values": {1, 2},
                    "requires": ["talairach"],
                },
            ),
            (
                "fstarg",
                bool,
                {
                    "help_string": "use vol from subject in --reg as target",
                    "argstr": "--fstarg",
                    "requires": ["regfile"],
                },
            ),
            (
                "invert",
                bool,
                {
                    "help_string": "invert the transform",
                    "argstr": "--inv",
                },
            ),
            (
                "no_resample",
                bool,
                {
                    "help_string": "do not resample, just change vox2ras matrix",
                    "argstr": "--no-resample",
                },
            ),
            (
                "interp",
                str,
                {
                    "help_string": (
                        "Interpolate the output based on the given method. Legal values are: "
                        "cubic, trilin and nearest."
                    ),
                    "argstr": "--interp {interp}",
                    "allowed_values": {"cubic", "nearest", "trilin"},
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    output_spec = SpecInfo(
        name="MRIVol2VolOutput",
        fields=[],
        bases=(ShellOutSpec,),
    )

    executable = "mri_vol2vol"
