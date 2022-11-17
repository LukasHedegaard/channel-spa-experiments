import subprocess

model_name = "resnet50"
for method_type in [
    "lrp",
    "weight",
    "taylor",
    "grad",
]:
    for norm in [
        True,
        False,
    ]:
        if not norm and method_type == "lrp":
            continue
        # fmt: off
        command = [
            "python", "main.py",
            "--train", 
            "--prune",
            "--arch", "resnet50",
            "--dataset", "oxfordflowers102",
            "--method-type", method_type,
            "--lr", "0.000156",
            "--batch-size", "4",
            "--epochs", "100",
            "--recovery_epochs", "50",
            # "--resume-from-ckpt", "weights/resnet50_oxfordflowers102_1.0.pth",
        ]
        # fmt: on
        if norm:
            command.append("--norm")

        subprocess.call(command)