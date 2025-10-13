# FIX META TAGS IN HTML FILES
# Moves meta charset and viewport from body to head

Write-Host ""
Write-Host "Fixing meta tags in HTML files..." -ForegroundColor Cyan
Write-Host ""

$htmlFiles = Get-ChildItem -Path "webapp" -Filter "*.html" -Recurse
$fixed = 0

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw
    $original = $content
    
    # Check if meta tags are in body and not in head
    if ($content -match '<body>.*?<meta') {
        # Extract meta tags from body
        $metaCharset = ""
        $metaViewport = ""
        
        if ($content -match '<body>.*?(<meta charset="[^"]+"\s*/?>)') {
            $metaCharset = $matches[1] -replace '\s*/?>', '>'
        }
        
        if ($content -match '<body>.*?(<meta name="viewport"[^>]+>)') {
            $metaViewport = $matches[1]
        }
        
        # If we found meta tags in body, move them to head
        if ($metaCharset -or $metaViewport) {
            # Add to head if not already there
            if ($metaCharset -and $content -notmatch '<head>.*<meta charset') {
                $content = $content -replace '(<head>)', "`$1`n    $metaCharset"
            }
            
            if ($metaViewport -and $content -notmatch '<head>.*<meta name="viewport"') {
                $content = $content -replace '(<head>)', "`$1`n    $metaViewport"
            }
            
            # Remove from body
            $content = $content -replace '<body>\s*<meta charset[^>]+>\s*', '<body>'
            $content = $content -replace '<body>\s*<meta name="viewport"[^>]+>\s*', '<body>'
            $content = $content -replace '<body>(\s*)<meta charset[^>]+>(\s*)<meta name="viewport"[^>]+>', '<body>$1'
        }
    }
    
    if ($content -ne $original) {
        $content | Out-File -FilePath $file.FullName -Encoding UTF8 -Force
        $fixed++
        Write-Host "Fixed: $($file.Name)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Completed! Fixed $fixed files" -ForegroundColor Cyan
Write-Host ""
