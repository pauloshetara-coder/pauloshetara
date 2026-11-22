# Instruções do projeto

## Link dos 37 mini e-books (obrigatório em todo vídeo de história)

Sempre que gerar um vídeo de história (roteiro, descrição do YouTube, posts, pacote de publicação),
inclua o link dos e-books exatamente assim (sempre citando que são 37 mini e-books), sem pedir e sem usar marcador como `[LINK DO EBOOK]`:

📚 Quer ir mais fundo? São 37 mini e-books com essas histórias: https://pay.kiwify.com.br/o5YIhPY

- Na descrição do YouTube: nas 2 primeiras linhas (antes do "mostrar mais") e repetido no fim.
- Em posts e legendas de redes sociais: no fim do texto.

## Vídeos: usar HyperFrames automaticamente

Sempre que for pedido para **montar, editar, animar ou renderizar um vídeo** (canal dark,
promoções, shorts/reels, legendas, títulos animados, linhas do tempo, mapas, gráficos,
slides em vídeo), use o **HyperFrames** como ferramenta padrão, no lugar de montar o vídeo
manualmente com ffmpeg, MoviePy ou outra ferramenta, sem precisar perguntar.

- As skills ficam em `.claude/skills/` (`hyperframes`, `hyperframes-cli`,
  `hyperframes-registry`, `media-use`). Carregue a skill `hyperframes` antes de começar.
- A CLI roda com `npx -y hyperframes <comando>` (requer Node.js 22+). Não precisa instalar.
- Fluxo: `npx -y hyperframes init` → escrever a composição em HTML → `npx -y hyperframes check`
  → `npx -y hyperframes render` para gerar o MP4.
- Imagens e cenas continuam vindo do Higgsfield/Nim ou dos arquivos enviados pelo usuário;
  o HyperFrames faz a montagem, animações, legendas, transições e trilha.
- Use ffmpeg só para tarefas simples de arquivo (converter formato, cortar, extrair áudio).

### Convivência com a skill `montagem-video-canal-dark`

As duas ficam ativas; nenhuma substitui a outra.

- **Montagem do canal dark** (imagens/clipes + narração → MP4 final com zoom, transições,
  trilha, tela final e legendas): use a skill `montagem-video-canal-dark`, como sempre.
- **HyperFrames**: use para todos os outros vídeos e para o que a skill do canal dark não
  cobre, como títulos animados, mapas, linhas do tempo, gráficos, legendas estilizadas e
  vinhetas. Esses trechos podem ser renderizados no HyperFrames e entrar na montagem do
  canal dark como clipes.
- Se o usuário pedir explicitamente uma das duas, use a que ele pediu.

Fonte: https://github.com/heygen-com/hyperframes (licença Apache 2.0, ver
`.claude/skills/HYPERFRAMES-LICENSE`). Para atualizar as skills, copie novamente a pasta
`skills/` desse repositório.
