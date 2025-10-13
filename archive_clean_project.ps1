# 🗂️ Скрипт 3: Архивирование CLEAN_PROJECT
# archive_clean_project.ps1

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "🗂️  АРХИВИРОВАНИЕ: CLEAN_PROJECT" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Шаг 1: Проверка существования CLEAN_PROJECT
Write-Host "🔍 Проверка наличия папки CLEAN_PROJECT..." -ForegroundColor Yellow

$cleanProjectPath = "CLEAN_PROJECT"

if (-Not (Test-Path $cleanProjectPath)) {
    Write-Host "   ⚠️  CLEAN_PROJECT не найдена, пропускаем" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "✅ Ничего не нужно делать" -ForegroundColor Green
    exit 0
}

Write-Host "   ✅ CLEAN_PROJECT найдена" -ForegroundColor Green

# Шаг 2: Создать папку archives
Write-Host ""
Write-Host "📁 Создание папки archives..." -ForegroundColor Yellow

$archivesPath = "archives"

if (-Not (Test-Path $archivesPath)) {
    New-Item -Path $archivesPath -ItemType Directory -Force | Out-Null
    Write-Host "   ✅ Папка archives создана" -ForegroundColor Green
} else {
    Write-Host "   ✅ Папка archives уже существует" -ForegroundColor Green
}

# Шаг 3: Получить список файлов для архивирования
Write-Host ""
Write-Host "📊 Анализ содержимого CLEAN_PROJECT..." -ForegroundColor Yellow

$files = Get-ChildItem -Path $cleanProjectPath -Recurse -File
$fileCount = $files.Count
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum
$totalSizeMB = [math]::Round($totalSize / 1MB, 2)

Write-Host "   📄 Файлов: $fileCount" -ForegroundColor White
Write-Host "   💾 Размер: $totalSizeMB МБ" -ForegroundColor White

# Шаг 4: Создать архив
Write-Host ""
Write-Host "🗜️  Создание архива..." -ForegroundColor Yellow

$timestamp = Get-Date -Format "yyyy_MM_dd_HHmmss"
$archiveName = "CLEAN_PROJECT_$timestamp.zip"
$archivePath = Join-Path $archivesPath $archiveName

try {
    # Используем .NET для создания архива (встроено в PowerShell)
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($cleanProjectPath, $archivePath)
    
    $archiveSize = (Get-Item $archivePath).Length
    $archiveSizeMB = [math]::Round($archiveSize / 1MB, 2)
    $compressionRatio = [math]::Round((1 - $archiveSize / $totalSize) * 100, 1)
    
    Write-Host "   ✅ Архив создан: $archiveName" -ForegroundColor Green
    Write-Host "   💾 Размер архива: $archiveSizeMB МБ" -ForegroundColor White
    Write-Host "   📊 Сжатие: $compressionRatio%" -ForegroundColor White
} catch {
    Write-Host "   ❌ Ошибка создания архива: $_" -ForegroundColor Red
    exit 1
}

# Шаг 5: Создать README в архиве
Write-Host ""
Write-Host "📝 Создание README для архива..." -ForegroundColor Yellow

$readmeContent = @"
# CLEAN_PROJECT - Архив дубликатов

**Дата архивирования:** $timestamp
**Исходная папка:** CLEAN_PROJECT/

## Содержимое

Этот архив содержит дублирующиеся файлы из проекта RULETTT, которые были
перемещены в папку CLEAN_PROJECT во время рефакторинга.

### Статистика

- **Файлов:** $fileCount
- **Размер (исходный):** $totalSizeMB МБ
- **Размер (архив):** $archiveSizeMB МБ
- **Сжатие:** $compressionRatio%

## Зачем архивировано?

Во время аудита проекта (PROJECT_AUDIT_REPORT.md) было обнаружено,
что папка CLEAN_PROJECT содержит дубликаты файлов из основного проекта.

Для улучшения структуры проекта эти файлы были архивированы, но не удалены
навсегда, чтобы можно было восстановить их при необходимости.

## Как восстановить?

1. Распакуйте этот архив в корень проекта:
   \`\`\`powershell
   Expand-Archive -Path "$archiveName" -DestinationPath "."
   \`\`\`

2. Папка CLEAN_PROJECT будет восстановлена со всеми файлами.

## Рекомендации

⚠️ **НЕ РЕКОМЕНДУЕТСЯ ВОССТАНАВЛИВАТЬ**, если вы не уверены, что вам
нужны эти файлы. Все актуальные файлы находятся в основном проекте.

## Контрольная сумма

- **SHA256:** $(Get-FileHash -Path $archivePath -Algorithm SHA256).Hash

---
🗑️ Безопасно удалить после 6 месяцев, если не потребовалось восстановление
"@

$readmePath = Join-Path $archivesPath "README_$timestamp.md"
$readmeContent | Out-File -FilePath $readmePath -Encoding UTF8 -Force

Write-Host "   ✅ README создан: README_$timestamp.md" -ForegroundColor Green

# Шаг 6: Создать .gitignore для archives
Write-Host ""
Write-Host "🔒 Создание .gitignore..." -ForegroundColor Yellow

$gitignorePath = Join-Path $archivesPath ".gitignore"
$gitignoreContent = @"
# Архивы не коммитим в Git (слишком большие)
*.zip
*.tar.gz
*.7z

# README можно коммитить
!README*.md
"@

$gitignoreContent | Out-File -FilePath $gitignorePath -Encoding UTF8 -Force
Write-Host "   ✅ .gitignore создан в archives/" -ForegroundColor Green

# Шаг 7: Удаление CLEAN_PROJECT
Write-Host ""
Write-Host "🗑️  Удаление CLEAN_PROJECT..." -ForegroundColor Yellow

$confirmation = Read-Host "❓ Удалить папку CLEAN_PROJECT? (да/нет)"

if ($confirmation -eq "да" -or $confirmation -eq "yes" -or $confirmation -eq "y") {
    try {
        Remove-Item -Path $cleanProjectPath -Recurse -Force
        Write-Host "   ✅ CLEAN_PROJECT удалена" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Ошибка удаления: $_" -ForegroundColor Red
        Write-Host "   ℹ️  Попробуйте вручную: Remove-Item -Path CLEAN_PROJECT -Recurse -Force" -ForegroundColor Blue
    }
} else {
    Write-Host "   ⏭️  Пропущено (можно удалить позже вручную)" -ForegroundColor Yellow
}

# Итоги
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ АРХИВИРОВАНИЕ ЗАВЕРШЕНО!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Результаты:" -ForegroundColor Yellow
Write-Host "   📦 Архив: archives/$archiveName" -ForegroundColor White
Write-Host "   💾 Размер: $archiveSizeMB МБ (было $totalSizeMB МБ)" -ForegroundColor White
Write-Host "   📄 Файлов: $fileCount" -ForegroundColor White
Write-Host "   📝 README: archives/README_$timestamp.md" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Следующие шаги:" -ForegroundColor Yellow
Write-Host "   1. Проверьте, что всё работает:" -ForegroundColor White
Write-Host "      python src/main.py" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. Если всё ок, можно удалить CLEAN_PROJECT:" -ForegroundColor White
Write-Host "      Remove-Item -Path CLEAN_PROJECT -Recurse -Force" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. Через 6 месяцев можно удалить архив:" -ForegroundColor White
Write-Host "      Remove-Item -Path archives/$archiveName" -ForegroundColor Gray
Write-Host ""
