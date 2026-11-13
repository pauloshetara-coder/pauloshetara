# Instruções do projeto

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

Fonte: https://github.com/heygen-com/hyperframes (licença Apache 2.0, ver
`.claude/skills/HYPERFRAMES-LICENSE`). Para atualizar as skills, copie novamente a pasta
`skills/` desse repositório.
