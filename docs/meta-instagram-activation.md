# Ativação futura da conexão Meta/Instagram

A Platéia funciona normalmente com **upload de arquivo, URL direta de mídia e links públicos**. A conexão profissional com Instagram é um recurso opcional, destinado a análises mais completas de conteúdos pertencentes à própria conta do usuário.

## Quando ativar

Ative esta integração somente quando houver um aplicativo Meta configurado para a Platéia e quando for necessário ler mídias de contas profissionais conectadas pelos próprios usuários.

## Credenciais necessárias

Configure no ambiente do projeto, nunca em campos públicos da aplicação:

| Variável | Uso |
|---|---|
| `META_INSTAGRAM_APP_ID` | Identifica o aplicativo Meta que inicia a autorização. |
| `META_INSTAGRAM_APP_SECRET` | Usado apenas no servidor para concluir a troca segura do código OAuth por token. |

## Referência de autorização oficial

A ativação deve usar o **Business Login for Instagram**, destinado a contas profissionais Business e Creator. A URL de autorização recebe `client_id`, `redirect_uri`, `response_type=code`, `scope` e um valor `state` para proteção contra CSRF. O código retornado é válido por uma hora e só pode ser utilizado uma vez. A troca de código, a conversão para token de longa duração e a renovação devem acontecer somente no servidor, onde o App Secret nunca é exposto ao navegador.

Para a primeira versão, solicite apenas `instagram_business_basic`, suficiente para a leitura de mídia da própria conta profissional. Outras permissões só devem ser solicitadas se uma funcionalidade futura exigir publicação, mensagens ou moderação.

Fonte oficial: [Meta — Business Login for Instagram](https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-instagram-login/business-login), atualizada em 13 de março de 2026.

## Fluxo esperado por usuário

1. A pessoa acessa **Instagram** na navegação da Platéia.
2. Ela escolhe conectar uma conta profissional Business ou Creator.
3. A Meta apresenta a tela oficial de autorização e informa os escopos solicitados.
4. A Platéia armazena o token somente de forma cifrada, associado ao usuário que autorizou a conexão.
5. A pessoa pode revogar a conexão; a Platéia remove o token armazenado e registra a revogação.

## Princípios de privacidade

>A conexão nunca deve compartilhar senhas com a Platéia. Cada usuário autoriza somente a própria conta e pode revogar o consentimento a qualquer momento.

Enquanto a integração não estiver ativada, mantenha como alternativas padrão o link público, o arquivo enviado pelo usuário e a URL direta de mídia.
