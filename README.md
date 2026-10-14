# corebot-container-smoke

Imagem mínima para testar a execução real do **Agente Container** do Corebot Py.

Não é um bot de script (não clona Git). O agente faz `docker pull` desta imagem, cria um container efêmero com UID `10001`, monta `/corebot/input` e `/corebot/output` e espera exit `0` + `result.json`.

## Imagem

| Campo no Control Room | Valor |
| --- | --- |
| Tipo de execução | Container |
| Repositório da imagem | `ghcr.io/angeloalves88/corebot-container-smoke` |
| Modo | Tag |
| Tag | `0.1.0` |
| Comando | (vazio — usa o ENTRYPOINT da imagem) |
| CPU | `0.5` |
| Memória (MB) | `256` |
| Timeout | `60` |

O repositório **não** leva tag nem digest no campo `image_repository`.

## Allowlist do agente

No host do Agente Container:

```
COREBOT_ALLOWED_REGISTRIES=ghcr.io/angeloalves88
```

`ghcr.io` sozinho também casa. Sem isso o agente recusa o pull (`POLICY_REJECTED`).

O pacote precisa estar **público** para o agente puxar sem `docker login` na sua conta. Se o pull falhar com 401, abra [as configurações do pacote](https://github.com/users/angeloalves88/packages/container/corebot-container-smoke/settings) e mude a visibilidade para Public.

## Teste local (sem o agente)

```bash
mkdir -p /tmp/corebot-smoke/input /tmp/corebot-smoke/output
printf '%s\n' '{"contract_version":1,"task_id":"local-1","bot":{"id":1,"name":"smoke"},"parameters":{"ping":"pong"}}' > /tmp/corebot-smoke/input/input.json

docker pull ghcr.io/angeloalves88/corebot-container-smoke:0.1.0
docker run --rm --user 10001:10001 \
  -v /tmp/corebot-smoke/input:/corebot/input:ro \
  -v /tmp/corebot-smoke/output:/corebot/output \
  -e COREBOT_INPUT_FILE=/corebot/input/input.json \
  -e COREBOT_OUTPUT_DIR=/corebot/output \
  ghcr.io/angeloalves88/corebot-container-smoke:0.1.0

cat /tmp/corebot-smoke/output/result.json
```

Esperado: stdout com `smoke concluido`, `result.json` com `"ok": true`, exit 0.
