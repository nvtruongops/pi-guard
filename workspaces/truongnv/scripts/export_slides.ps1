$pptxPath = (Resolve-Path 'workspaces/truongnv/reports/tasks_for_meeting_6/PI-GUARD-Present-Meeting-6.pptx').Path
$exportDir = Join-Path (Resolve-Path 'workspaces/truongnv/reports/tasks_for_meeting_6').Path 'exported_slides'

if (-not (Test-Path $exportDir)) {
    New-Item -ItemType Directory -Path $exportDir -Force | Out-Null
}

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $pres = $ppt.Presentations.Open($pptxPath, [Microsoft.Office.Core.MsoTriState]::msoTrue, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # 18 = ppSaveAsPNG
    $pres.SaveAs($exportDir, 18)
    $pres.Close()
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
    Write-Host "[+] Successfully exported slides to $exportDir"
    Get-ChildItem -Path $exportDir | Measure-Object | ForEach-Object { Write-Host "[*] Exported $($_.Count) slide images." }
} catch {
    Write-Error "[-] Export failed: $_"
}
