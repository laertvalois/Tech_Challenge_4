# Script PowerShell para SUBSTITUIR COMPLETAMENTE o repositório GitHub
# Este script faz um push forçado que substitui tudo no GitHub pelo estado local
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "PUSH COMPLETO PARA GITHUB" -ForegroundColor Cyan
Write-Host "Substituindo todo o repositório remoto" -ForegroundColor Yellow
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
Write-Host "⚠️  ATENÇÃO: Este script irá SUBSTITUIR completamente o repositório remoto!" -ForegroundColor Yellow
Write-Host "Todos os arquivos no GitHub serão substituídos pelos arquivos locais." -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Deseja continuar? (S/N)"
if ($confirm -ne "S" -and $confirm -ne "s") {
    Write-Host "Operação cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Verificando status do repositório local..." -ForegroundColor Yellow
git status

Write-Host ""
Write-Host "Adicionando TODOS os arquivos (incluindo .streamlit/config.toml)..." -ForegroundColor Yellow

# Forçar adição do config.toml mesmo que esteja no .gitignore
if (Test-Path ".streamlit\config.toml") {
    Write-Host "✅ .streamlit/config.toml encontrado - forçando adição..." -ForegroundColor Green
    git add -f .streamlit/config.toml
} else {
    Write-Host "⚠️  .streamlit/config.toml não encontrado!" -ForegroundColor Yellow
}

# Adicionar todos os outros arquivos
git add -A

Write-Host ""
Write-Host "Arquivos que serão commitados:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "Fazendo commit de TODAS as alterações..." -ForegroundColor Yellow
$commitMessage = "Atualização completa: correção do menu sidebar no Streamlit Cloud - background claro forçado"
git commit -m $commitMessage

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Aviso: Pode não haver alterações para commitar." -ForegroundColor Yellow
    Write-Host "Criando commit vazio para forçar atualização..." -ForegroundColor Yellow
    git commit --allow-empty -m $commitMessage
}

Write-Host ""
Write-Host "Garantindo que a branch é 'main'..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "Fazendo PUSH FORÇADO para GitHub (substituindo tudo)..." -ForegroundColor Yellow
Write-Host "⚠️  Isso irá sobrescrever o histórico remoto!" -ForegroundColor Red
Write-Host ""
$confirm2 = Read-Host "Confirma o push forçado? (S/N)"
if ($confirm2 -ne "S" -and $confirm2 -ne "s") {
    Write-Host "Operação cancelada." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Executando: git push --force -u origin main" -ForegroundColor Cyan
git push --force -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✅ Push forçado realizado com sucesso!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repositório: https://github.com/laertvalois/Tech_Challenge_4" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Último commit:" -ForegroundColor Yellow
    git log --oneline -1
    Write-Host ""
    Write-Host "⚠️  IMPORTANTE:" -ForegroundColor Yellow
    Write-Host "1. Aguarde alguns minutos para o Streamlit Cloud atualizar" -ForegroundColor Yellow
    Write-Host "2. Verifique se o arquivo .streamlit/config.toml está no GitHub" -ForegroundColor Yellow
    Write-Host "3. Se necessário, faça um redeploy manual no Streamlit Cloud" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Erro ao fazer push forçado." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "- Problemas de autenticação (use Personal Access Token)"
    Write-Host "- Verifique se você tem permissão para fazer push forçado"
    Write-Host "- Tente executar: git push --force -u origin main manualmente"
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
