# AUTO-FIX ALL LINT ISSUES
# This script automatically fixes all remaining lint warnings

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AUTO-FIX LINT ISSUES" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalFixed = 0
$filesModified = 0

# ============================================
# FIX 1: Add -webkit- prefix for backdrop-filter
# ============================================
Write-Host "Step 1: Adding Safari compatibility..." -ForegroundColor Yellow

$htmlFiles = Get-ChildItem -Path "webapp" -Filter "*.html" -Recurse
$backdropFixed = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Add -webkit-backdrop-filter before backdrop-filter
    $content = $content -replace '(\s+)backdrop-filter:', '$1-webkit-backdrop-filter: blur(10px);$1backdrop-filter:'
    $content = $content -replace '(\s+)-webkit-backdrop-filter: blur\(10px\);(\s+)-webkit-backdrop-filter:', '$1-webkit-backdrop-filter:'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $backdropFixed++
        $filesModified++
    }
}

$totalFixed += $backdropFixed
Write-Host "  Fixed: $backdropFixed files (Safari backdrop-filter)" -ForegroundColor Green

# ============================================
# FIX 2: Ensure all external links have rel="noopener noreferrer"
# ============================================
Write-Host "Step 2: Fixing external links security..." -ForegroundColor Yellow

$linksFixed = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Fix links with target="_blank" but missing or incomplete rel
    $content = $content -replace 'target="_blank"\s*>', 'target="_blank" rel="noopener noreferrer">'
    $content = $content -replace 'target="_blank"\s+(?!rel=)', 'target="_blank" rel="noopener noreferrer" '
    $content = $content -replace 'rel="noopener"\s+class=', 'rel="noopener noreferrer" class='
    $content = $content -replace 'rel="noopener">', 'rel="noopener noreferrer">'
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $linksFixed++
        if ($original -eq $content) { $filesModified++ }
    }
}

$totalFixed += $linksFixed
Write-Host "  Fixed: $linksFixed files (external links)" -ForegroundColor Green

# ============================================
# FIX 3: Fix HTML meta tags in head
# ============================================
Write-Host "Step 3: Fixing HTML meta tags..." -ForegroundColor Yellow

$metaFixed = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Fix meta tags that are in body (move to head)
    # Pattern: <body> followed by meta tags - move them to </head> area
    if ($content -match '<body>(\s*)<meta charset') {
        $content = $content -replace '(<head>)', '$1`n    <meta charset="UTF-8">'
        $content = $content -replace '<body>\s*<meta charset[^>]+>', '<body>'
    }
    
    if ($content -match '<body>.*?<meta name="viewport"') {
        if ($content -notmatch '<head>.*<meta name="viewport"') {
            $content = $content -replace '(<meta charset="UTF-8">)', '$1`n    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
        }
        $content = $content -replace '<body>(\s*)<meta name="viewport"[^>]+>', '<body>$1'
    }
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $metaFixed++
    }
}

$totalFixed += $metaFixed
Write-Host "  Fixed: $metaFixed files (meta tags)" -ForegroundColor Green

# ============================================
# FIX 4: Extract ALL inline styles to external CSS
# ============================================
Write-Host "Step 4: Extracting ALL inline styles to CSS..." -ForegroundColor Yellow

$stylesExtracted = 0
$cssContent = @"
/* Auto-generated CSS from inline styles */
/* Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") */

/* Utility Classes */
.mt-5 { margin-top: 5px; }
.mt-10 { margin-top: 10px; }
.mt-15 { margin-top: 15px; }
.mt-20 { margin-top: 20px; }
.mt-25 { margin-top: 25px; }
.mt-30 { margin-top: 30px; }
.mb-5 { margin-bottom: 5px; }
.mb-10 { margin-bottom: 10px; }
.mb-15 { margin-bottom: 15px; }
.mb-20 { margin-bottom: 20px; }
.mb-25 { margin-bottom: 25px; }
.p-15 { padding: 15px; }
.m-20-0 { margin: 20px 0; }
.m-15-0 { margin: 15px 0; }

/* Layout Utilities */
.flex { display: flex; }
.flex-1 { flex: 1; }
.gap-10 { gap: 10px; }
.gap-15 { gap: 15px; }
.justify-between { justify-content: space-between; }
.align-center { align-items: center; }
.text-left { text-align: left; }
.w-100 { width: 100%; }
.pos-rel { position: relative; }

/* Typography */
.fs-08 { font-size: 0.8em; }
.fs-085 { font-size: 0.85em; }
.fs-09 { font-size: 0.9em; }
.fs-15 { font-size: 1.5em; }
.fw-bold { font-weight: bold; }
.opacity-07 { opacity: 0.7; }
.opacity-08 { opacity: 0.8; }

/* Colors */
.color-orange { color: #FF9800; }
.color-green { color: #4CAF50; }
.bg-warning { background: rgba(255,193,7,0.1); padding: 15px; }
.bg-overlay { background: rgba(255,255,255,0.2); }

/* Chat Styles */
.chat-container {
    height: 300px;
    overflow-y: auto;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 15px;
    margin: 20px 0;
}

.chat-message {
    margin-bottom: 15px;
}

.chat-input {
    flex: 1;
    padding: 12px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    color: white;
}

.chat-status {
    opacity: 0.7;
    font-size: 0.9em;
    margin-top: 5px;
}

/* Progress Bars */
.progress-75 .progress-fill { width: 75% !important; }
.progress-60 .progress-fill { width: 60% !important; }
.progress-68 .progress-fill { width: 68% !important; }
.progress-67 .progress-fill { width: 67% !important; }

/* Form Styles */
.form-label {
    display: block;
    margin: 10px 0;
}

.form-input-compact {
    flex: 1;
    padding: 8px;
    border-radius: 5px;
    border: 1px solid rgba(255,255,255,0.3);
    background: rgba(255,255,255,0.1);
    color: white;
}

.form-label-inline {
    font-size: 0.9em;
    opacity: 0.8;
}

.form-section {
    margin: 20px 0;
}

/* Platform Details */
.platform-details {
    margin-top: 30px;
}

.platform-list {
    text-align: left;
    margin: 15px 0;
}

/* User Avatar */
.user-avatar-add {
    background: rgba(255,255,255,0.2);
    font-size: 1.5em;
    cursor: pointer;
}

.user-avatar-add:hover {
    background: rgba(255,255,255,0.3);
}

/* Stat Card Variants */
.stat-card-compact {
    margin-bottom: 10px;
    padding: 15px;
}

.stat-card-warning {
    padding: 15px;
    background: rgba(255,193,7,0.1);
}

/* Task Item */
.task-item {
    display: flex;
    gap: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    margin-bottom: 10px;
}

.task-title {
    font-weight: bold;
    margin-bottom: 5px;
}

.task-desc {
    font-size: 0.8em;
    opacity: 0.8;
}

.task-progress {
    width: 100%;
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
}

.task-progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    transition: width 0.3s ease;
}
"@

# Create extracted-styles.css in webapp
$cssPath = "webapp\extracted-styles.css"
$cssContent | Out-File -FilePath $cssPath -Encoding UTF8 -Force
Write-Host "  Created: extracted-styles.css" -ForegroundColor Green

# Now replace ALL common inline styles with classes (expanded list)
$patternsToReplace = @(
    @{ Pattern = 'style="margin-bottom: 20px"'; Class = 'class="mb-20"' },
    @{ Pattern = 'style="margin-bottom: 15px"'; Class = 'class="mb-15"' },
    @{ Pattern = 'style="margin-bottom: 10px; padding: 15px;"'; Class = 'class="stat-card-compact"' },
    @{ Pattern = 'style="margin-bottom: 10px"'; Class = 'class="mb-10"' },
    @{ Pattern = 'style="margin-bottom: 5px"'; Class = 'class="mb-5"' },
    @{ Pattern = 'style="padding: 15px; background: rgba(255,193,7,0.1);"'; Class = 'class="bg-warning"' },
    @{ Pattern = 'style="padding: 15px;"'; Class = 'class="p-15"' },
    @{ Pattern = 'style="width: 75%;"'; Class = 'class="progress-75"' },
    @{ Pattern = 'style="width: 60%;"'; Class = 'class="progress-60"' },
    @{ Pattern = 'style="width: 68%;"'; Class = 'class="progress-68"' },
    @{ Pattern = 'style="width: 67%;"'; Class = 'class="progress-67"' },
    @{ Pattern = 'style="background: rgba(255,255,255,0.2); font-size: 1.5em;"'; Class = 'class="user-avatar-add"' },
    @{ Pattern = 'style="height: 300px; overflow-y: auto; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 15px; margin: 20px 0;"'; Class = 'class="chat-container"' },
    @{ Pattern = 'style="flex: 1; padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white;"'; Class = 'class="chat-input"' },
    @{ Pattern = 'style="display: flex; gap: 10px; align-items: center; margin-top: 5px;"'; Class = 'class="flex gap-10 align-center mt-5"' },
    @{ Pattern = 'style="display: flex; gap: 10px;"'; Class = 'class="flex gap-10"' },
    @{ Pattern = 'style="display: flex; gap: 15px"'; Class = 'class="flex gap-15"' },
    @{ Pattern = 'style="font-size: 0.9em; opacity: 0.8;"'; Class = 'class="form-label-inline"' },
    @{ Pattern = 'style="flex: 1; padding: 8px; border-radius: 5px; border: 1px solid rgba(255,255,255,0.3); background: rgba(255,255,255,0.1); color: white;"'; Class = 'class="form-input-compact"' },
    @{ Pattern = 'style="opacity: 0.7; font-size: 0.9em; margin-top: 5px;"'; Class = 'class="chat-status"' },
    @{ Pattern = 'style="display: flex; gap: 15px; padding: 15px; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; margin-bottom: 10px;"'; Class = 'class="task-item"' },
    @{ Pattern = 'style="position: relative"'; Class = 'class="pos-rel"' },
    @{ Pattern = 'style="margin-top: 30px"'; Class = 'class="mt-30"' },
    @{ Pattern = 'style="color: #4caf50; margin-bottom: 15px"'; Class = 'class="color-green mb-15"' },
    @{ Pattern = 'style="font-weight: bold; margin-bottom: 5px"'; Class = 'class="task-title"' },
    @{ Pattern = 'style="font-size: 0.8em; opacity: 0.8"'; Class = 'class="task-desc"' },
    @{ Pattern = 'style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-top: 8px;"'; Class = 'class="task-progress"' },
    @{ Pattern = 'style="height: 100%; width: 75%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); transition: width 0.3s ease;"'; Class = 'class="task-progress-bar"' },
    @{ Pattern = 'style="height: 100%; width: 60%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); transition: width 0.3s ease;"'; Class = 'class="task-progress-bar"' },
    @{ Pattern = 'style="margin-top: 30px;"'; Class = 'class="mt-30"' },
    @{ Pattern = 'style="margin-top: 25px;"'; Class = 'class="mt-25"' },
    @{ Pattern = 'style="margin-top: 20px;"'; Class = 'class="mt-20"' },
    @{ Pattern = 'style="margin-top: 15px;"'; Class = 'class="mt-15"' },
    @{ Pattern = 'style="margin-top: 10px;"'; Class = 'class="mt-10"' },
    @{ Pattern = 'style="margin-bottom: 25px;"'; Class = 'class="mb-25"' },
    @{ Pattern = 'style="text-align: left; margin: 15px 0;"'; Class = 'class="platform-list"' },
    @{ Pattern = 'style="font-size: 0.85em; opacity: 0.7; margin-top: 5px;"'; Class = 'class="fs-085 opacity-07 mt-5"' },
    @{ Pattern = 'style="font-size: 0.9em;"'; Class = 'class="fs-09"' },
    @{ Pattern = 'style="color: #FF9800;"'; Class = 'class="color-orange"' },
    @{ Pattern = 'style="margin: 20px 0;"'; Class = 'class="form-section"' },
    @{ Pattern = 'style="display: block; margin: 10px 0;"'; Class = 'class="form-label"' },
    @{ Pattern = 'style="width: 100%; margin-bottom: 10px;"'; Class = 'class="w-100 mb-10"' },
    @{ Pattern = 'style="width: 100%;"'; Class = 'class="w-100"' }
)

$inlineStylesFixed = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Add link to extracted-styles.css in <head> if not present
    if ($content -match '<head>' -and $content -notmatch 'extracted-styles.css') {
        $content = $content -replace '(<head>)', '$1`n    <link rel="stylesheet" href="extracted-styles.css">'
    }
    
    # Replace inline styles with classes
    foreach ($replacement in $patternsToReplace) {
        $content = $content -replace [regex]::Escape($replacement.Pattern), $replacement.Class
    }
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $inlineStylesFixed++
    }
}

$totalFixed += $inlineStylesFixed
Write-Host "  Fixed: $inlineStylesFixed files (inline styles)" -ForegroundColor Green

# ============================================
# FIX 5: Update markdown files formatting
# ============================================
Write-Host "Step 5: Fixing markdown formatting..." -ForegroundColor Yellow

$mdFiles = Get-ChildItem -Path . -Filter "*.md" -Recurse -Exclude "node_modules","venv",".venv","Lib","Include"
$markdownFixed = 0

foreach ($file in $mdFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Fix common markdown issues (but keep them readable)
    # Remove trailing punctuation from headings (but keep emoji)
    $content = $content -replace '(#{1,6}\s+[^!\n]+)!(\s*)$', '$1$2'
    
    # Add blank lines around code fences
    $content = $content -replace '([^\n])\n```', '$1`n`n```'
    $content = $content -replace '```\n([^\n])', '```\n`n$1'
    
    # Fix ordered lists
    $content = $content -replace '(\n)(\d+)\.\s', '$11. '
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $markdownFixed++
    }
}

$totalFixed += $markdownFixed
Write-Host "  Fixed: $markdownFixed files (markdown)" -ForegroundColor Green

# ============================================
# FIX 6: Check RULETTT_ONLINE folder
# ============================================
Write-Host "Step 6: Checking RULETTT_ONLINE folder..." -ForegroundColor Yellow

if (Test-Path "RULETTT_ONLINE") {
    $choice = Read-Host "RULETTT_ONLINE folder found. Delete it? (y/n)"
    if ($choice -eq "y" -or $choice -eq "yes" -or $choice -eq "Y") {
        # Archive first
        if (!(Test-Path "archives")) {
            New-Item -ItemType Directory -Path "archives" | Out-Null
        }
        
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $timestamp = Get-Date -Format "yyyy_MM_dd_HHmmss"
        $archivePath = "archives/RULETTT_ONLINE_$timestamp.zip"
        
        [System.IO.Compression.ZipFile]::CreateFromDirectory("RULETTT_ONLINE", $archivePath)
        Write-Host "  Archived: $archivePath" -ForegroundColor Green
        
        Remove-Item -Path "RULETTT_ONLINE" -Recurse -Force
        Write-Host "  Deleted: RULETTT_ONLINE folder" -ForegroundColor Green
    } else {
        Write-Host "  Skipped: RULETTT_ONLINE folder kept" -ForegroundColor Yellow
    }
} else {
    Write-Host "  OK: No RULETTT_ONLINE folder found" -ForegroundColor Green
}

# ============================================
# FINAL REPORT
# ============================================
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AUTO-FIX COMPLETED!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Summary:" -ForegroundColor Yellow
Write-Host "  Safari compatibility: $backdropFixed files" -ForegroundColor White
Write-Host "  External links:       $linksFixed files" -ForegroundColor White
Write-Host "  Meta tags:            $metaFixed files" -ForegroundColor White
Write-Host "  Inline styles:        $inlineStylesFixed files" -ForegroundColor White
Write-Host "  Markdown:             $markdownFixed files" -ForegroundColor White
Write-Host "  ---" -ForegroundColor Gray
Write-Host "  Total fixes:          $totalFixed" -ForegroundColor Green
Write-Host "  Files modified:       $filesModified" -ForegroundColor Green
Write-Host ""

Write-Host "Created files:" -ForegroundColor Yellow
Write-Host "  - webapp/extracted-styles.css" -ForegroundColor White
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test the website: http://localhost:8080" -ForegroundColor Cyan
Write-Host "  2. Check extracted-styles.css is loaded" -ForegroundColor Cyan
Write-Host "  3. Verify all links open in new tabs safely" -ForegroundColor Cyan
Write-Host ""

Write-Host "All lint issues should now be resolved!" -ForegroundColor Green
Write-Host ""
