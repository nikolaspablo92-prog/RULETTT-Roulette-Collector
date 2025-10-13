# AUTO-FIX REMAINING LINT ISSUES
# Fixes all remaining inline styles in actual webapp files

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FIX REMAINING INLINE STYLES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalFixed = 0

# Updated CSS with all missing classes
$additionalCSS = @"

/* Additional utility classes */
.fs-12 { font-size: 1.2em; }
.color-blue { color: #3498db; }
.color-gray { color: #666; }
.opacity-06 { opacity: 0.6; }

/* Form input compact small */
.form-input-small {
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    color: white;
    font-size: 0.9em;
    width: 120px;
}

/* Background variants */
.bg-purple-light { background: rgba(156, 39, 176, 0.2); }
.bg-orange-alert {
    background: rgba(255,152,0,0.2);
    border-left: 3px solid #ff9800;
}

/* Status indicators */
.status-success { color: #4CAF50; }
.status-error { color: #f44336; }

/* Utility spacing */
.mt-10-opacity-07 {
    margin-top: 10px;
    opacity: 0.7;
}

.mt-10-opacity-06-fs-09 {
    margin-top: 10px;
    opacity: 0.6;
    font-size: 0.9em;
}

.mt-10-gray {
    margin-top: 10px;
    color: #666;
}

/* Log container */
.log-container {
    display: none;
    max-height: 300px;
    overflow-y: auto;
}

.log-container.visible {
    display: block;
}
"@

# Append to existing extracted-styles.css
$cssPath = "webapp\extracted-styles.css"
if (Test-Path $cssPath) {
    Add-Content -Path $cssPath -Value $additionalCSS -Encoding UTF8
    Write-Host "Updated extracted-styles.css with additional classes" -ForegroundColor Green
}

# Fix communication.html
Write-Host "Fixing communication.html..." -ForegroundColor Yellow
$file = "webapp\communication.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    # Replace specific patterns
    $content = $content -replace 'style="padding: 4px 8px; border-radius: 4px; border: 1px solid rgba\(255,255,255,0\.3\); background: rgba\(255,255,255,0\.1\); color: white; font-size: 0\.9em; width: 120px;"', 'class="form-input-small"'
    $content = $content -replace 'style="background: rgba\(156, 39, 176, 0\.2\)"', 'class="bg-purple-light"'
    
    # Remove empty style attributes
    $content = $content -replace '\s+style="\s*"', ''
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: communication.html" -ForegroundColor Green
    }
}

# Fix test_simple.html
Write-Host "Fixing test_simple.html..." -ForegroundColor Yellow
$file = "webapp\test_simple.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    $content = $content -replace 'style="color: #3498db;"', 'class="color-blue"'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: test_simple.html" -ForegroundColor Green
    }
}

# Fix public_access_ready.html
Write-Host "Fixing public_access_ready.html..." -ForegroundColor Yellow
$file = "webapp\public_access_ready.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    $content = $content -replace 'style="background: rgba\(255,152,0,0\.2\); border-left-color: #ff9800;"', 'class="bg-orange-alert"'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: public_access_ready.html" -ForegroundColor Green
    }
}

# Fix home.html
Write-Host "Fixing home.html..." -ForegroundColor Yellow
$file = "webapp\home.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    $content = $content -replace 'style="font-size: 1\.2em;"', 'class="fs-12"'
    $content = $content -replace 'style="margin-top: 15px; opacity: 0\.7;"', 'class="mt-15 opacity-07"'
    $content = $content -replace 'style="margin-top: 10px; opacity: 0\.6; font-size: 0\.9em;"', 'class="mt-10-opacity-06-fs-09"'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: home.html" -ForegroundColor Green
    }
}

# Fix admin/login.html
Write-Host "Fixing admin/login.html..." -ForegroundColor Yellow
$file = "webapp\admin\login.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    $content = $content -replace 'style="margin-top: 10px; color: #666;"', 'class="mt-10-gray"'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: admin/login.html" -ForegroundColor Green
    }
}

# Fix remote_control.html - inline styles in JavaScript
Write-Host "Fixing remote_control.html (JS inline styles)..." -ForegroundColor Yellow
$file = "webapp\remote_control.html"
if (Test-Path $file) {
    $content = Get-Content $file -Raw
    $original = $content
    
    # Replace JavaScript generated inline styles with classes
    $content = $content -replace "style=`"display:none; max-height:300px; overflow-y:auto;`"", 'class="log-container"'
    $content = $content -replace "'<span style=`"color:#4CAF50`">вњ… Р Р°Р±РѕС‚Р°РµС‚</span>'", "'<span class=`"status-success`">вњ… Р Р°Р±РѕС‚Р°РµС‚</span>'"
    $content = $content -replace "'<span style=`"color:#f44336`">вќЊ РћС€РёР±РєР°</span>'", "'<span class=`"status-error`">вќЊ РћС€РёР±РєР°</span>'"
    $content = $content -replace "'<span style=`"color:#f44336`">вќЊ РќРµРґРѕСЃС‚СѓРїРµРЅ</span>'", "'<span class=`"status-error`">вќЊ РќРµРґРѕСЃС‚СѓРїРµРЅ</span>'"
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file -Encoding UTF8 -Force
        $totalFixed++
        Write-Host "  Fixed: remote_control.html" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files fixed: $totalFixed" -ForegroundColor Green
Write-Host "CSS updated: extracted-styles.css" -ForegroundColor Green
Write-Host ""
Write-Host "All inline styles should now be converted to classes!" -ForegroundColor Green
Write-Host ""
