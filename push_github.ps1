# Script PowerShell para fazer push das alterações para GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Push para GitHub - Tech Challenge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se estamos no diretório correto
if (-not (Test-Path "app\app.py")) {
    Write-Host "Erro: Execute este script no diretório raiz do projeto!" -ForegroundColor Red
    exit 1
}

# Configurar remote
$repoUrl = "https://github.com/laertvalois/Tech_Challenge_4.git"
Write-Host "Repositório: $repoUrl" -ForegroundColor Yellow
Write-Host ""

# Verificar se o remote existe
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Adicionando remote..." -ForegroundColor Yellow
    git remote add origin $repoUrl
} else {
    Write-Host "Remote já configurado: $existingRemote" -ForegroundColor Green
}

Write-Host ""
Write-Host "Verificando status do repositório..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "Adicionando todos os arquivos..." -ForegroundColor Yellow
git add -A

Write-Host ""
Write-Host "Arquivos modificados:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "Fazendo commit..." -ForegroundColor Yellow
$commitMessage = "Melhorias: campos opcionais, menu lateral mais largo, formulário reorganizado, tradução de campos no PDF"
git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Aviso: Pode não haver alterações para commitar ou commit já foi feito." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Garantindo que a branch é 'main'..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "Fazendo push para GitHub..." -ForegroundColor Yellow
Write-Host "Você pode ser solicitado a fazer login no GitHub." -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Push realizado com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repositório: https://github.com/laertvalois/Tech_Challenge_4" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Último commit:" -ForegroundColor Yellow
    git log --oneline -1
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- Problemas de autenticação (use Personal Access Token)"
    Write-Host "- Verifique se você tem permissão para fazer push"
    Write-Host "- Tente executar: git push -u origin main manualmente"
    Write-Host ""
    Write-Host "Para autenticar:" -ForegroundColor Cyan
    Write-Host "1. GitHub → Settings → Developer settings → Personal access tokens"
    Write-Host "2. Generate new token (classic)"
    Write-Host "3. Marque a permissão 'repo'"
    Write-Host "4. Use o token como senha quando solicitado"
}

Write-Host ""
Write-Host "Pressione qualquer tecla para sair..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
