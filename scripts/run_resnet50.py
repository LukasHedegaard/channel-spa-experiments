import subprocess
from pathlib import Path

model_name = "resnet50"
adapter_init_range = str(1e-4)

# for seed in ["1", "2", "3"]:
for seed in ["1"]:
    for method_type, norm in [
        # ("taylor", True),
        # ("taylor", False),
        ("grad", True),
        # ("grad", False),
        # ("weight", True),
        # ("weight", False),
        # ("lrp", True),
    ]:
        for dataset, lr, bs, epochs, recovery_epocs in [
            ("cifar10", str(0.01 / 256 * 64), "64", "40", "20"),
            ("oxfordflowers102", str(0.01 / 256 * 6), "6", "100", "50"),
            ("catsanddogs", str(0.01 / 256 * 16), "16", "100", "50"),
            # ("stanfordcars", str(0.01 / 256 * 6), "6", "100", "50"),
            # ("cifar100", str(0.01 / 256 * 64), "64", "60", "30"),
        ]:
            for adapter_config in ["sppara"]:  # [None, "8", "32", "sppara"]:
                # fmt: off
                command = [
                    "python", "main_resnet.py",
                    # "--train",  # Added conditionally later in script
                    "--epochs", epochs,
                    "--prune",
                    "--recovery_epochs", recovery_epocs,
                    "--arch", model_name,
                    "--dataset", dataset,
                    "--method-type", method_type,
                    "--lr", lr,
                    "--batch-size", bs,
                    "--seed", seed,
                ]
                if adapter_config == "sppara":
                    command.extend([
                        "--sppara",
                        "--splora-init-range", adapter_init_range,
                    ])
                    ckpt = f"weights/sppara_{model_name}_{dataset}_1.0_seed={seed}.pth"
                elif adapter_config is not None:
                    command.extend([
                        "--splora",
                        "--splora-rank", adapter_config,
                        "--splora-init-range", adapter_init_range,
                    ])
                    ckpt = f"weights/splora_r{adapter_config}_{model_name}_{dataset}_1.0_seed={seed}.pth"
                else:
                    ckpt = f"weights/{model_name}_{dataset}_1.0_seed={seed}.pth"
                # fmt: on
                if norm:
                    command.append("--norm")

                if Path(ckpt).exists():
                    command.extend(["--resume-from-ckpt", ckpt])
                else:
                    command.extend(["--train"])

                print(command)
                subprocess.call(command)