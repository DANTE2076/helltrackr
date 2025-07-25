import time
import base58
import itertools
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator, Bip39WordsNum
from nacl.signing import SigningKey

# Mapa Leet simplificado solo con sustituciones reales
leet_map = {
    'A': ['A', '4'],
    'E': ['E', '3'],
    'G': ['G', '6'],
    'I': ['I', '1'],
    'L': ['L', '1'],
    'O': ['O', '0'],
    'S': ['S', '5'],
    'T': ['T', '7'],
    'Z': ['Z', '2'],
}

def generar_variaciones(prefix, usar_leet):
    opciones = []
    for letra in prefix.upper():
        if usar_leet and letra in leet_map:
            opciones.append(leet_map[letra] + [letra.lower()])
        else:
            opciones.append([letra, letra.lower()])
    return {''.join(p) for p in itertools.product(*opciones)}

def generar_wallet():
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12)
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    sk = SigningKey(seed_bytes[:32])
    pk = sk.verify_key
    priv_key = sk.encode()
    pub_key = pk.encode()
    return (
        mnemonic.ToStr(),
        base58.b58encode(pub_key).decode(),
        base58.b58encode(priv_key).decode(),
        priv_key.hex(),
    )

# === MAIN ===
if __name__ == "__main__":
    base_prefix = input("🆔 ¿Qué texto quieres buscar? (Ej: HOOT, HELLTRACKR): ").strip().upper()
    if not base_prefix.isalnum():
        print("❌ Prefijo inválido. Debe ser alfanumérico.")
        exit(1)

    try:
        length = int(input(f"🔢 ¿Cuántos caracteres quieres buscar? (1-{len(base_prefix)}): "))
        assert 1 <= length <= len(base_prefix)
    except:
        print("❌ Valor no válido. Se usará 4 por defecto.")
        length = 4

    usar_leet = input("🎭 ¿Activar modo 'leet-style'? (y/N): ").lower() == "y"

    target_prefix = base_prefix[:length]
    print(f"\n🎯 Buscando una dirección que empiece por algo como: {target_prefix}")
    if usar_leet:
        print("🌀 Modo Leet activado: se buscarán también variaciones como 3, 1, 0, etc.")

    # Generar variaciones por cada nivel de coincidencia
    variaciones_por_longitud = {}
    for i in range(length, 2, -1):  # Solo desde 3 letras en adelante
        variaciones_por_longitud[i] = generar_variaciones(target_prefix[:i], usar_leet)

    mejores = {i: None for i in variaciones_por_longitud}
    start_time = time.time()
    intentos = 0

    while True:
        mnemonic, pub, priv32, priv64 = generar_wallet()
        intentos += 1

        for i in variaciones_por_longitud:
            if any(pub.startswith(v) for v in variaciones_por_longitud[i]):
                if mejores[i] is None or pub != mejores[i]:
                    mejores[i] = pub
                    elapsed = round(time.time() - start_time, 2)
                    print(f"\n🌟 ¡Nueva mejor coincidencia de {i} letras!")
                    print(f"📫 Dirección pública: {pub}")
                    print(f"🔑 Clave privada (32b): {priv32}")
                    print(f"🔐 Clave privada extendida (64b): {priv64}")
                    print(f"🧠 Mnemónica: {mnemonic}")
                    print(f"💾 Guardada en: wallets_{base_prefix.lower()}_{i}.txt")

                    with open(f"wallets_{base_prefix.lower()}_{i}.txt", "a") as f:
                        f.write(f"{pub} | {priv32} | {mnemonic}\n")
                break

        if intentos % 10000 == 0:
            elapsed = time.time() - start_time
            hashrate = round(intentos / elapsed, 2)
            print(f"{intentos} intentos... última dirección: {pub} | ⛏️ {hashrate} direcciones/seg")