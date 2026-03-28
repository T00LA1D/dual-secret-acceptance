# ToolAid Lab Pro Windows

Full suite scaffold for Flipper device control, signal capture, automation, and experimentation.

## Run as a Linux app (simulation mode)

```bash
python ToolAidLauncher.py --mode capture --duration 1
python ToolAidLauncher.py --mode experiment --loops 2
```

The launcher currently uses a local `MockFlipperDevice` so it can run without physical hardware.
