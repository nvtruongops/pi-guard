"""Check the ingress diagram's visible flowchart and three-label contracts."""

from pathlib import Path
from xml.etree import ElementTree as ET

report = Path(__file__).resolve().parents[1]
repo = report.parent
source = report / "reports" / "PI_GUARD_INGRESS_ARCHITECTURE.drawio"
diagram = ET.parse(source)
pages = diagram.findall("diagram")
assert len(pages) == 8
cells = {cell.get("id"): cell for page in pages for cell in page.findall(".//mxCell")}
edges = [cell for cell in cells.values() if cell.get("edge") == "1"]

for cell_id in ("one_l2_score", "l2_gate", "mini_dashboard", "mini_allow", "mini_block"):
    assert "shape=rect;" in cells[cell_id].get("style", ""), cell_id
assert all("dashed=1;" not in edge.get("style", "") for edge in edges)
assert all("mxgraph.aws4" not in cell.get("style", "") for cell in cells.values())
assert "UML Activity" not in cells["arch_subtitle"].get("value", "")
assert "POST-ALLOW" not in cells["mini_external_region"].get("value", "")
assert cells["mini_external_region"].get("value") == "<b>EXTERNAL SYSTEMS</b>"

scores = cells["mini_e_scores_dashboard"]
assert scores.get("source") == "mini_api_aggregate" and scores.get("target") == "mini_dashboard"
for cell_id in ("mini_l3", "mini_dashboard", "one_l3_scores", "l3m_predictions"):
    assert all(label in cells[cell_id].get("value", "") for label in (
        "Benign", "Prompt Injection", "Jailbreak"
    )), cell_id
assert {edge.get("value") for edge in edges if edge.get("source") == "mini_final_decision"} == {
    "[ALLOW]", "[BLOCK]"
}

preview = report / "reports" / "PI_GUARD_INGRESS_ARCHITECTURE.png"
assert preview.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
assert not (report / source.name).exists()
assert not (report / preview.name).exists()
assert not (repo / "Github-Page" / "assets" / "ingress_architecture_review1_summary_vertical.png").exists()
print("PASS: 8 pages, ISO-informed shape semantics, three labels, solid score flow, single canonical source and PNG")
