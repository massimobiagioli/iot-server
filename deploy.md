# IoT Server - Deployment Guide per Raspberry Pi

Questa guida fornisce istruzioni per installare l'IoT Server su un Raspberry Pi in modo **semplice e automatizzato**.

## 🚀 Installazione Rapida (Consigliata)

### Prerequisiti Minimi
- Raspberry Pi 3B+ o superiore con Raspberry Pi OS
- Connessione internet
- Accesso SSH o terminale

### Installazione Automatica

1. **Clona il repository:**
   ```bash
   cd /home/pi
   git clone https://github.com/massimobiagioli/iot-server.git
   cd iot-server
   ```

2. **Esegui l'installazione automatica:**
   ```bash
   make deploy
   ```

   **Personalizzazione Directory di Installazione (Opzionale):**
   
   Per installare in una directory diversa da `/home/pi/iot-server`, imposta la variabile di ambiente `INSTALL_DIR`:
   
   **Temporanea (solo per la sessione corrente):**
   ```bash
   export INSTALL_DIR="/home/massimo/github/iot-server"
   make deploy
   ```
   
   **Permanente (per tutte le sessioni future):**
   ```bash
   # Aggiungi al file di profilo bash
   echo 'export INSTALL_DIR="/home/massimo/github/iot-server"' >> ~/.bashrc
   source ~/.bashrc
   make deploy
   ```
   
   **Oppure in un singolo comando:**
   ```bash
   INSTALL_DIR="/home/massimo/github/iot-server" make deploy
   ```

3. **Configura MQTT (se necessario):**
   ```bash
   nano .env
   # Modifica MQTT_HOST, MQTT_USERNAME, MQTT_PASSWORD
   sudo systemctl restart iot-server
   ```

**✅ Fatto! Il server è ora disponibile su `http://your-pi-ip:8000`**

---

## 📋 Installazione Manuale Dettagliata

*Usa questa sezione solo se l'installazione automatica non funziona o vuoi personalizzare l'installazione.*

### Hardware Richiesto
- Raspberry Pi 3B+ o superiore (consigliato Pi 4)
- MicroSD card da almeno 16GB (classe 10)
- Alimentatore ufficiale Raspberry Pi
- Connessione di rete (Ethernet o WiFi)

### Software Richiesto
- Raspberry Pi OS (Bullseye o Bookworm)
- Accesso SSH o desktop

## 🔧 Installazione Manuale

*Le seguenti operazioni sono automatizzate dallo script `make deploy`. Usa questa sezione solo per troubleshooting o personalizzazioni.*

<details>
<summary><strong>Clicca per espandere le istruzioni manuali</strong></summary>

### 1. Preparazione del Sistema

```bash
# Aggiorna il sistema
sudo apt update && sudo apt upgrade -y

# Installa dipendenze di sistema
sudo apt install -y git curl build-essential libssl-dev libffi-dev python3-dev nodejs npm sqlite3
```

### 2. Installazione Python 3.11+

```bash
# Verifica versione Python
python3 --version

# Se necessario, installa Python 3.11
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev
```

### 3. Setup Applicazione

```bash
# Clone repository (se non già fatto)
cd /home/pi
git clone https://github.com/massimobiagioli/iot-server.git
cd iot-server

# Crea ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate

# Installa dipendenze
pip install --upgrade pip
pip install -r requirements.txt

# Setup database
npm install  # Se package.json esiste
npx prisma generate
npx prisma db push
```

### 4. Configurazione Servizio

```bash
# Crea file di servizio systemd
sudo tee /etc/systemd/system/iot-server.service > /dev/null << EOF
[Unit]
Description=IoT Server FastAPI Application
After=network.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=/home/pi/iot-server
Environment=PATH=/home/pi/iot-server/.venv/bin
ExecStart=/home/pi/iot-server/.venv/bin/python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Abilita e avvia servizio
sudo systemctl daemon-reload
sudo systemctl enable iot-server.service
sudo systemctl start iot-server.service
```

</details>

## ⚙️ Configurazione MQTT

Dopo l'installazione (automatica o manuale), configura il broker MQTT:

```bash
# Modifica il file di configurazione
nano .env
```

Contenuto del file `.env`:
```bash
# MQTT Configuration
MQTT_HOST=192.168.1.100  # IP del tuo broker MQTT
MQTT_PORT=1883
MQTT_USERNAME=your_username  # Se necessario
MQTT_PASSWORD=your_password  # Se necessario

# Database Configuration
DATABASE_URL=file:./production.db
```

Dopo la modifica, riavvia il servizio:
```bash
sudo systemctl restart iot-server
```

## 🧪 Test dell'Installazione

### Verifica che l'applicazione funzioni

```bash
# Test locale
curl http://localhost:8000/health

# Test da altro dispositivo (sostituisci con l'IP del Pi)
curl http://192.168.1.100:8000/health
```

### Accedi all'interfaccia web

Apri il browser e vai a: `http://your-pi-ip:8000`

### Test MQTT

```bash
# Installa mosquitto client
sudo apt install -y mosquitto-clients

# Invia messaggio di test
mosquitto_pub -h localhost -t device_status -m '{
  "payload": {
    "device_type": "esp32",
    "device_id": "test123",
    "device_name": "test_device"
  },
  "timestamp": 1234567890,
  "event_type": "connected"
}'
```

## 🔧 Gestione del Servizio

### Comandi Utili

```bash
# Visualizza log in tempo reale
sudo journalctl -u iot-server -f

# Stato del servizio
sudo systemctl status iot-server

# Riavvia il servizio
sudo systemctl restart iot-server

# Ferma/avvia il servizio
sudo systemctl stop iot-server
sudo systemctl start iot-server
```

## 🔄 Aggiornamenti

```bash
cd /home/pi/iot-server
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
npx prisma generate
npx prisma db push
sudo systemctl restart iot-server
```

## 🐛 Troubleshooting

### Problemi Comuni

```bash
# Servizio non si avvia - controlla log
sudo journalctl -u iot-server -n 50

# Problemi di permessi
sudo chown -R pi:pi /home/pi/iot-server

# Riavvia tutto
sudo systemctl restart iot-server
```

### Configurazioni Avanzate

<details>
<summary><strong>Nginx + SSL, Firewall, Sicurezza (clicca per espandere)</strong></summary>

#### Nginx Reverse Proxy
```bash
sudo apt install -y nginx
sudo tee /etc/nginx/sites-available/iot-server > /dev/null << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/iot-server /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

#### SSL con Let's Encrypt
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### Firewall
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8000
```

</details>

---

## 🎉 **Installazione Completata!**

**Il tuo IoT Server è ora attivo su:** `http://your-pi-ip:8000`

**Per supporto:** Controlla i log con `sudo journalctl -u iot-server -f`
