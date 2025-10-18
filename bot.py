#!/usr/bin/env python3
import os
import argparse
from datetime import datetime

def parse_size(s: str):
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except Exception:
        raise argparse.ArgumentTypeError("Size must look like 1024x768")

def main():
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a virtual X display (Xvfb) or an existing DISPLAY."
    )
    parser.add_argument("--start-xvfb", action="store_true",
                        help="Start a fresh virtual monitor with Xvfb using pyvirtualdisplay.")
    parser.add_argument("--display", default=None,
                        help="DISPLAY to attach to (e.g., :99 or :1). If --start-xvfb is used, this is ignored.")
    parser.add_argument("--size", type=parse_size, default="1024x768",
                        help="Virtual screen size WxH when using --start-xvfb (default: 1024x768).")
    parser.add_argument("--outfile", default=None,
                        help="Output PNG path (default: ./screenshot-YYYYmmdd-HHMMSS.png).")
    parser.add_argument("--method", choices=["auto", "pyautogui", "mss"], default="auto",
                        help="Capture method. 'auto' tries PyAutoGUI then MSS.")
    args = parser.parse_args()

    outfile = args.outfile or f"screenshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"

    display_ctx = None
    if args.start_xvfb:
        # Start a brand-new virtual monitor
        from pyvirtualdisplay import Display
        w, h = args.size
        # You can change backend="xvfb" explicitly if desired.
        display_ctx = Display(visible=0, size=(w, h))
        display_ctx.start()
        print(f"[info] Started Xvfb on DISPLAY={os.environ.get('DISPLAY')} with size {w}x{h}")
    else:
        # Attach to an existing DISPLAY if provided
        if args.display:
            os.environ["DISPLAY"] = args.display
        disp = os.environ.get("DISPLAY")
        if not disp:
            raise SystemExit("No DISPLAY set. Use --start-xvfb or pass --display :N")

    try:
        method_used = None
        if args.method in ("auto", "pyautogui"):
            try:
                import pyautogui
                img = pyautogui.screenshot()  # captures the root window of current $DISPLAY
                img.save(outfile)
                method_used = "pyautogui"
            except Exception as e:
                if args.method == "pyautogui":
                    raise
                print(f"[warn] PyAutoGUI capture failed: {e}")

        if method_used is None and args.method in ("auto", "mss"):
            try:
                import mss
                with mss.mss() as sct:
                    # monitor 0 = full virtual desktop; on Xvfb there’s usually just one monitor
                    shot = sct.grab(sct.monitors[0])
                    from PIL import Image
                    Image.frombytes("RGB", (shot.width, shot.height), shot.rgb).save(outfile)
                    method_used = "mss"
            except Exception as e:
                if args.method == "mss":
                    raise
                print(f"[warn] MSS capture failed: {e}")

        if method_used is None:
            raise SystemExit("No screenshot method succeeded. Try installing scrot or use --method mss.")

        print(f"[ok] Saved screenshot via {method_used} → {outfile}")

    finally:
        if display_ctx is not None:
            display_ctx.stop()
            print("[info] Stopped Xvfb")

if __name__ == "__main__":
    main()

