## Instalação do Google Cloud

Comandos baseados no tutorial fornecido pela propria google [https://cloud.google.com/sdk/docs/install?hl=pt-br#deb](tutorial)

### Atualiza os pacotes e instala os pacotes necessarios para adicionar o gcloud
```bash
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates gnupg curl
```

### Adiciona novas origens necessarios para o pacote gcloud e suas extensões
```bash
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```

### Intala o pacote base do gcloud
```bash
sudo apt-get update && sudo apt-get install google-cloud-cli
```

### Inicializando gcloud
```bash
gcloud init
```
projet id: `optimal-pursuit-429516-c8`