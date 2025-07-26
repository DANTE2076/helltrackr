# 💀 HellTrackr

> **Version:** 1.0.0  
> **Author:** Helltrackr  
> **Donations (SOL):** `HELLg3wgaxNf7zewEbgxLXDqEVRd9ymwT5KgbxFuLxZn`

**HellTrackr** is a fast and efficient vanity address generator for the Solana blockchain. Customize your desired prefix, enable optional leetspeak substitutions, and mine stylish addresses in seconds.

---

## 🧪 How It Works

HellTrackr brute-forces valid Solana addresses derived from BIP39 mnemonics. It continuously generates new wallets until it finds a public key that matches your target prefix (with or without leet-style variations).

### 🔧 Features

- Custom prefix search (e.g. `DANTE`)
- Optional leetspeak support (`D4NT3`, `d4nt3`, etc.)
- Saves all valid results with:
  - Public key
  - Base58 private key
  - Mnemonic phrase
- Shows speed every 10,000 attempts

---

## ▶️ Usage

Just run the executable and follow the prompts:

```
🆔 What text do you want to find? (e.g., HOOT, HELLTRACKR): DANTE
🔢 How many characters do you want to match? (1-5): 5
🎭 Enable 'leet-style' mode? (y/N): y
```

The script will keep running and print whenever a better match is found. All matches are saved in `wallets_<prefix>_<length>.txt`, for example:

```
wallets_dante_5.txt
```

Each line in the file includes:

```
<PublicKey> | <PrivateKey32> | <Mnemonic>
```

---

## ⚙️ Build From Source

### 🔩 Requirements

```bash
pip install -r requirements.txt
```

### 🛠 Build Executable with PyInstaller

```bash
pyinstaller --onefile generador.py --name helltrackr \
  --add-data "<path_to_bip39_wordlists>/*.txt;bip_utils/bip/bip39/wordlist" \
  --hidden-import=coincurve._libsecp256k1 \
  --hidden-import=coincurve._cffi_backend \
  --hidden-import=_cffi_backend
```

---

## 👨‍💻 Developer Info

- **Author:** Helltrackr  
- **Version:** `1.0.0`  
- **Solana Wallet (donations welcome):**  
  `HELLg3wgaxNf7zewEbgxLXDqEVRd9ymwT5KgbxFuLxZn`

---

## 📄 License

MIT License — feel free to fork, use or contribute!

---

## 🎉 Support

If this project helps you or makes you smile, send some SOL to support development:

**SOL address:** `HELLg3wgaxNf7zewEbgxLXDqEVRd9ymwT5KgbxFuLxZn`


