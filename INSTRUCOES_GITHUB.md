# 📤 Instruções para Subir o Projeto no GitHub

## ✅ Passo 1: Commit Realizado

O commit inicial já foi feito localmente. Agora você precisa criar o repositório no GitHub e fazer o push.

## 🔧 Passo 2: Criar Repositório no GitHub

### Opção A: Via Interface Web do GitHub

1. Acesse https://github.com e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Preencha:
   - **Repository name:** `tech-challenge-obesity` (ou outro nome de sua preferência)
   - **Description:** "Sistema Preditivo de Obesidade - Tech Challenge"
   - **Visibility:** Escolha Public ou Private
   - **NÃO marque** "Initialize this repository with a README" (já temos um)
5. Clique em **"Create repository"**

### Opção B: Via GitHub CLI (se tiver instalado)

```bash
gh repo create tech-challenge-obesity --public --description "Sistema Preditivo de Obesidade - Tech Challenge"
```

## 🚀 Passo 3: Conectar e Fazer Push

Após criar o repositório no GitHub, execute os seguintes comandos:

```bash
# Adicionar o remote (substitua SEU_USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU_USUARIO/tech-challenge-obesity.git

# Ou se preferir usar SSH:
# git remote add origin git@github.com:SEU_USUARIO/tech-challenge-obesity.git

# Verificar o remote
git remote -v

# Fazer push do código
git branch -M main
git push -u origin main
```

## 📝 Passo 4: Atualizar LINKS_ENTREGA.txt

Depois de fazer o push, atualize o arquivo `LINKS_ENTREGA.txt` com o link do seu repositório:

```
3. REPOSITÓRIO GITHUB:
   https://github.com/SEU_USUARIO/tech-challenge-obesity
```

## 🔐 Autenticação

Se for solicitado login:
- **Token de acesso pessoal:** Use um Personal Access Token (PAT) do GitHub
- Para criar um token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Permissões necessárias: `repo` (acesso completo a repositórios)

## ✅ Verificação

Após o push, verifique se tudo foi enviado corretamente:
- Acesse seu repositório no GitHub
- Verifique se todos os arquivos estão lá
- Confirme que o README.md está sendo exibido

## 🎯 Próximos Passos

1. ✅ Repositório criado no GitHub
2. ⏭️ Fazer deploy no Streamlit Cloud
3. ⏭️ Atualizar LINKS_ENTREGA.txt com todos os links
4. ⏭️ Gravar vídeo de apresentação

