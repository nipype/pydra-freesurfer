import os, pytest
from pathlib import Path
from ..applyvoltransform import ApplyVolTransform


@pytest.mark.xfail(
    "FREESURFER_HOME" not in os.environ,
    reason="no Freesurfer found",
    raises=FileNotFoundError,
)
@pytest.mark.parametrize("inputs, outputs", [])
def test_ApplyVolTransform(test_data, inputs, outputs):
    in_file = Path(test_data) / "test.nii.gz"
    if inputs is None:
        inputs = {{}}
    for key, val in inputs.items():
        try:
            inputs[key] = eval(val)
        except:
            pass
    task = {self.interface_name}(in_file=in_file, **inputs)
    assert set(task.generated_output_names) == set(
        ["return_code", "stdout", "stderr"] + outputs
    )
    res = task()
    print("RESULT: ", res)
    for out_nm in outputs:
        assert getattr(res.output, out_nm).exists()
