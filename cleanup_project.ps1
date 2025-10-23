# 🧹 ПОЛНАЯ ОЧИСТКА ПРОЕКТА RULETTT
# cleanup_project.ps1

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🧹 ПОЛНАЯ ОЧИСТКА ПРОЕКТА RULETTT" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$totalDeleted = 0
$totalSize = 0

# ═══════════════════════════════════════════════════════════
# ШАГ 1: Удаление Python кэша
# ═══════════════════════════════════════════════════════════
Write-Host "🗑️  Шаг 1/7: Удаление Python кэша..." -ForegroundColor Yellow

$pycacheFiles = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
$pycCount = $pycacheFiles.Count

if ($pycCount -gt 0) {
    foreach ($folder in $pycacheFiles) {
        $size = (Get-ChildItem -Path $folder.FullName -Recurse -File | Measure-Object -Property Length -Sum).Sum
        $totalSize += $size
        Remove-Item -Path $folder.FullName -Recurse -Force
        $totalDeleted++
    }
    Write-Host "   ✅ Удалено $pycCount папок __pycache__" -ForegroundColor Green
} else {
    Write-Host "   ✅ Нет __pycache__" -ForegroundColor Green
}

# ═══════════════════════════════════════════════════════════
# ШАГ 2: Удаление дублирующихся GUIDE/README/INSTRUCTIONS
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "📄 Шаг 2/7: Удаление дублирующихся документов..." -ForegroundColor Yellow

$docsToDelete = @(
    "ACTION_PLAN.md",
    "ADMIN_GUIDE.md",
    "ADMIN_QUICK_GUIDE.md",
    "AI_CHAT_INTEGRATION_COMPLETE.md",
    "api_search_guide.md",
    "BOT_ARCHITECTURE.md",
    "COLLABORATION_READY.txt",
    "COMPREHENSIVE_FEATURES_GUIDE.md",
    "console_analysis_report.txt",
    "CROSS_PLATFORM_READY.md",
    "DATA_SOURCE_EXPLAINED.md",
    "DOCUMENTATION_INDEX.md",
    "EXTERNAL_ACCESS_GUIDE.md",
    "FILES_CREATED.md",
    "FINAL_SUCCESS_GUIDE.txt",
    "FIX_INSTRUCTIONS.txt",
    "FOR_FRIEND.txt",
    "GITHUB_CODESPACES_GUIDE.txt",
    "GLOBAL_CHAT_READY.md",
    "IMPLEMENTATION_SUMMARY.md",
    "LAUNCH_ALL_FEATURES.txt",
    "MACOS_DEBUG_GUIDE.md",
    "MACOS_USER_GUIDE.md",
    "NEXT_STEPS_PADDYPOWER.md",
    "NGROK_SETUP_GUIDE.md",
    "ONLINE_COLLABORATION.txt",
    "ONLINE_SETUP_GUIDE.txt",
    "QUICK_EXTERNAL_SETUP.md",
    "QUICK_JOIN.txt",
    "QUICK_ONLINE_START.txt",
    "QUICK_START.txt",
    "QUICK_START_BOT.md",
    "QUICK_START_NOW.md",
    "QUICK_UPDATE.txt",
    "QUICK_VS_CODE_JOIN.md",
    "README_API_SEARCH.md",
    "README_BOT.md",
    "README_XPATH.md",
    "READY_TO_USE.md",
    "REMOTE_ACCESS_COMPLETE.md",
    "REMOTE_ACCESS_SETUP.md",
    "SAVE_STATS_GUIDE.txt",
    "setup_guide.md",
    "setup_instructions.md",
    "SHARE_PROJECT.txt",
    "START.md",
    "START_COLLECTOR.txt",
    "START_HERE.md",
    "STEP_2_CREATE_GITHUB_REPO.txt",
    "STEP_4_CREATE_CODESPACE.txt",
    "SUMMARY.md",
    "SYSTEM_READY.md",
    "SYSTEM_READY.txt",
    "TEAM_AI_CHAT_READY.md",
    "TEAM_GUIDE.md",
    "TEAM_INVITATION.md",
    "TESTING_CHECKLIST.md",
    "TESTING_REAL_DATA.md",
    "TESTING_UPDATE.md",
    "UPDATE_STATS_FUNCTION.txt",
    "URGENT_MACOS_INSTRUCTIONS.md",
    "VERSION_COMPARISON.md",
    "VIEW_DATA_CHEATSHEET.md",
    "VIEW_DATA_GUIDE.md",
    "VS_CODE_COLLABORATION.md",
    "VS_CODE_READY.md",
    "WHATS_NEW_PADDYPOWER.md",
    "WHY_NOT_VISIBLE.txt",
    "XPATH_FOUND.md"
)

$deletedDocs = 0
foreach ($doc in $docsToDelete) {
    if (Test-Path $doc) {
        $size = (Get-Item $doc).Length
        $totalSize += $size
        Remove-Item -Path $doc -Force
        $deletedDocs++
        $totalDeleted++
    }
}
Write-Host "   ✅ Удалено $deletedDocs дублирующихся документов" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ШАГ 3: Удаление дублирующихся Python скриптов
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "🐍 Шаг 3/7: Удаление дублирующихся Python скриптов..." -ForegroundColor Yellow

$scriptsToDelete = @(
    "api_finder.py",
    "api_hunting_guide.py",
    "api_server_macos.py",
    "AUTO_COLLECTOR_GUIDE.py",
    "auto_console_collector.py",
    "browser_api_guide.py",
    "CONSOLE_METHOD.py",
    "console_guide.py",
    "css_to_xpath.py",
    "debug_api.py",
    "final_single_table_system.py",
    "final_summary.py",
    "fix_single_table_system.py",
    "HOW_TO_GET_XPATH.py",
    "HOW_TO_USE_CONSOLE_DATA.py",
    "OPERA_CONSOLE_METHOD.py",
    "OPERA_FIXED_CODE.py",
    "paddypower_analyzer.py",
    "PROBLEM_SOLVED.py",
    "quick_api_setup.py",
    "quick_scraper_test.py",
    "READY_TO_TEST.py",
    "SCRAPER_INSTRUCTIONS.py",
    "SCRAPER_READY.py",
    "setup_casino.py",
    "setup_external_access.py",
    "setup_pragmatic_auth.py",
    "simple_api_finder.py",
    "single_table_collector.py",
    "spinandgo_analyzer.py",
    "start_api.py",
    "strict_single_table.py",
    "SUCCESS_RESULTS.py",
    "universal_api_setup.py",
    "web_scraper_single_roulette.py"
)

$deletedScripts = 0
foreach ($script in $scriptsToDelete) {
    if (Test-Path $script) {
        $size = (Get-Item $script).Length
        $totalSize += $size
        Remove-Item -Path $script -Force
        $deletedScripts++
        $totalDeleted++
    }
}
Write-Host "   ✅ Удалено $deletedScripts дублирующихся скриптов" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ШАГ 4: Удаление дублирующихся bat/sh файлов
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "⚙️  Шаг 4/7: Удаление дублирующихся запускных файлов..." -ForegroundColor Yellow

$batchToDelete = @(
    "create_clean_version.bat",
    "launch_macos.sh",
    "launch_rulettt.py",
    "launch_windows.bat",
    "prepare_for_friend.bat",
    "setup_public_access.bat",
    "start_codespaces.sh",
    "start_public_rulettt.bat",
    "test_system.bat"
)

$deletedBatch = 0
foreach ($batch in $batchToDelete) {
    if (Test-Path $batch) {
        $size = (Get-Item $batch).Length
        $totalSize += $size
        Remove-Item -Path $batch -Force
        $deletedBatch++
        $totalDeleted++
    }
}
Write-Host "   ✅ Удалено $deletedBatch запускных файлов" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ШАГ 5: Удаление дублирующихся JSON конфигов
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "📋 Шаг 5/7: Удаление дублирующихся конфигов..." -ForegroundColor Yellow

$configsToDelete = @(
    "casino_setup.json",
    "paddypower_config.json",
    "pragmatic_auth_template.json",
    "pragmatic_play_config.json",
    "roulette_console_data_example.json"
)

$deletedConfigs = 0
foreach ($config in $configsToDelete) {
    if (Test-Path $config) {
        $size = (Get-Item $config).Length
        $totalSize += $size
        Remove-Item -Path $config -Force
        $deletedConfigs++
        $totalDeleted++
    }
}
Write-Host "   ✅ Удалено $deletedConfigs конфигов" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ШАГ 6: Удаление дублирующихся JavaScript
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "🟨 Шаг 6/7: Удаление дублирующихся JavaScript файлов..." -ForegroundColor Yellow

$jsToDelete = @(
    "paddypower_collector.js",
    "paddypower_collector_v2.js"
)

$deletedJS = 0
foreach ($js in $jsToDelete) {
    if (Test-Path $js) {
        $size = (Get-Item $js).Length
        $totalSize += $size
        Remove-Item -Path $js -Force
        $deletedJS++
        $totalDeleted++
    }
}
Write-Host "   ✅ Удалено $deletedJS JavaScript файлов" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ШАГ 7: Архивация больших файлов/папок
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "📦 Шаг 7/7: Проверка больших файлов/папок..." -ForegroundColor Yellow

# CLEAN_Roulette_Collector.zip
if (Test-Path "CLEAN_Roulette_Collector.zip") {
    $size = (Get-Item "CLEAN_Roulette_Collector.zip").Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "   ⚠️  Найден архив CLEAN_Roulette_Collector.zip ($sizeMB МБ)" -ForegroundColor Yellow
    Write-Host "      Рекомендуется удалить или переместить в archives/" -ForegroundColor Gray
}

# ngrok.exe
if (Test-Path "ngrok.exe") {
    $size = (Get-Item "ngrok.exe").Length
    $sizeMB = [math]::Round($size / 1MB, 2)
    Write-Host "   ⚠️  Найден ngrok.exe ($sizeMB МБ)" -ForegroundColor Yellow
    Write-Host "      Рекомендуется переместить в tools/ или удалить" -ForegroundColor Gray
}

# node_modules/
if (Test-Path "node_modules") {
    $nodeSize = (Get-ChildItem -Path "node_modules" -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $nodeSizeMB = [math]::Round($nodeSize / 1MB, 2)
    Write-Host "   ⚠️  Найдена папка node_modules/ ($nodeSizeMB МБ)" -ForegroundColor Yellow
    Write-Host "      Рекомендуется удалить, если не используете Node.js" -ForegroundColor Gray
}

Write-Host "   ✅ Проверка завершена" -ForegroundColor Green

# ═══════════════════════════════════════════════════════════
# ИТОГИ
# ═══════════════════════════════════════════════════════════
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ ОЧИСТКА ЗАВЕРШЕНА!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

Write-Host "📊 Статистика очистки:" -ForegroundColor Yellow
Write-Host "   🗑️  Удалено файлов/папок: $totalDeleted" -ForegroundColor White
Write-Host "   💾 Освобождено места: $totalSizeMB МБ" -ForegroundColor White
Write-Host ""

Write-Host "📋 Детали:" -ForegroundColor Yellow
Write-Host "   Python кэш:      $pycCount папок" -ForegroundColor Gray
Write-Host "   Документы:       $deletedDocs файлов" -ForegroundColor Gray
Write-Host "   Python скрипты:  $deletedScripts файлов" -ForegroundColor Gray
Write-Host "   Bat/sh файлы:    $deletedBatch файлов" -ForegroundColor Gray
Write-Host "   JSON конфиги:    $deletedConfigs файлов" -ForegroundColor Gray
Write-Host "   JavaScript:      $deletedJS файлов" -ForegroundColor Gray
Write-Host ""

Write-Host "🔄 Следующие шаги:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1️⃣  Архивировать CLEAN_PROJECT:" -ForegroundColor White
Write-Host "      .\archive_clean_project.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   2️⃣  Организовать тесты:" -ForegroundColor White
Write-Host "      .\refactor_tests.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   3️⃣  Разделить зависимости:" -ForegroundColor White
Write-Host "      .\refactor_requirements.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   4️⃣  Создать __init__.py:" -ForegroundColor White
Write-Host "      .\create_init_files.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "   5️⃣  Проверить проект:" -ForegroundColor White
Write-Host "      py test_system.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
