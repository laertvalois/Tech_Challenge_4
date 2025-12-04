# Script para fazer push imediato para GitHub
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
Write-Host "Configurando remote: $repoUrl" -ForegroundColor Yellow

# Remover remote existente se houver
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote existente encontrado. Removendo..." -ForegroundColor Yellow
    git remote remove origin
}

# Adicionar remote
git remote add origin $repoUrl
if ($LASTEXITCODE -ne 0) {
    Write-Host "Aviso: Pode já estar configurado ou erro ao adicionar remote" -ForegroundColor Yellow
}

# Verificar remote
Write-Host ""
Write-Host "Remote configurado:" -ForegroundColor Green
git remote -v
Write-Host ""

# Adicionar todos os arquivos
Write-Host "Adicionando arquivos..." -ForegroundColor Yellow
git add -A

# Verificar status
Write-Host ""
Write-Host "Status do repositório:" -ForegroundColor Yellow
git status --short

# Fazer commit
Write-Host ""
Write-Host "Fazendo commit..." -ForegroundColor Yellow
git commit -m "Evolução do app Streamlit: menu lateral, páginas separadas, campos profissional/paciente, exportação PDF e melhorias de UX"

# Renomear branch para main
Write-Host ""
Write-Host "Garantindo que a branch é 'main'..." -ForegroundColor Yellow
git branch -M main

# Fazer push
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
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- Problemas de autenticação (use Personal Access Token)"
    Write-Host "- Verifique se você tem permissão para fazer push"
    Write-Host "- Tente executar: git push -u origin main manualmente"
}
