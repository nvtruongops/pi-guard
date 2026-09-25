"""
workspaces/truongnv/scripts/export_slides_to_images.py

Exports each slide of PI-GUARD-Present-Meeting-6-Light.pptx to a PNG image
using Microsoft PowerPoint COM Automation.
"""

import os
import sys

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def export_slides(pptx_path, output_dir):
    abs_pptx = os.path.abspath(pptx_path)
    abs_out = os.path.abspath(output_dir)
    os.makedirs(abs_out, exist_ok=True)
    
    import comtypes.client
    
    print(f"[*] Opening PowerPoint COM to export: {abs_pptx}")
    ppt_app = comtypes.client.CreateObject("PowerPoint.Application")
    # ppSaveAsPNG = 18, ppSaveAsJPG = 17
    deck = ppt_app.Presentations.Open(abs_pptx, True, False, False)
    deck.SaveAs(abs_out, 18)
    deck.Close()
    ppt_app.Quit()
    print(f"[+] Successfully exported slides to: {abs_out}")


if __name__ == "__main__":
    pptx = "workspaces/truongnv/reports/tasks_for_meeting_6/PI-GUARD-Present-Meeting-6-Light.pptx"
    out_dir = "workspaces/truongnv/reports/tasks_for_meeting_6/exported_slides"
    if len(sys.argv) > 1:
        pptx = sys.argv[1]
    if len(sys.argv) > 2:
        out_dir = sys.argv[2]
        
    try:
        export_slides(pptx, out_dir)
    except Exception as e:
        print(f"[-] COM Export failed: {e}")
        # Try powershell fallback script if comtypes not installed
