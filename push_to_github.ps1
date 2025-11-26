# Script PowerShell para fazer push do projeto para GitHub
# Execute este script após criar o repositório no GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Push para GitHub - Tech Challenge" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar informações do usuário
$githubUser = Read-Host "Digite seu username do GitHub"
$repoName = Read-Host "Digite o nome do repositório (ex: tech-challenge-obesity)"

if ([string]::IsNullOrWhiteSpace($githubUser) -or [string]::IsNullOrWhiteSpace($repoName)) {
    Write-Host "Erro: Username e nome do repositório são obrigatórios!" -ForegroundColor Red
    exit 1
}

# URL do repositório
$repoUrl = "https://github.com/$githubUser/$repoName.git"

Write-Host ""
Write-Host "Configurando remote..." -ForegroundColor Yellow

# Verificar se o remote já existe
$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' já existe. Removendo..." -ForegroundColor Yellow
    git remote remove origin
}

# Adicionar remote
git remote add origin $repoUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao adicionar remote. Verifique se o repositório existe no GitHub." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Remote configurado: $repoUrl" -ForegroundColor Green

# Renomear branch para main (se necessário)
Write-Host ""
Write-Host "Renomeando branch para 'main'..." -ForegroundColor Yellow
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
    Write-Host "Repositório: https://github.com/$githubUser/$repoName" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Próximos passos:" -ForegroundColor Yellow
    Write-Host "1. Atualize o arquivo LINKS_ENTREGA.txt com o link do repositório"
    Write-Host "2. Faça o deploy no Streamlit Cloud"
    Write-Host "3. Atualize os links no LINKS_ENTREGA.txt"
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- Repositório não existe no GitHub (crie primeiro em github.com)"
    Write-Host "- Problemas de autenticação (use Personal Access Token)"
    Write-Host "- Verifique se você tem permissão para fazer push"
}

