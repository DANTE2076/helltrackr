__version__ = "1.0.0"

import time
import base58
import itertools
from datetime import datetime
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator, Bip39WordsNum
from nacl.signing import SigningKey

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

def generate_variations(prefix, use_leet):
    options = []
    for letter in prefix.upper():
        if use_leet and letter in leet_map:
            options.append(leet_map[letter] + [letter.lower()])
        else:
            options.append([letter, letter.lower()])
    return {''.join(p) for p in itertools.product(*options)}

def generate_wallet():
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

if __name__ == "__main__":

    base_prefix = input("🆔 What prefix are you looking for? (e.g., HOOT, HELLTRACKR): ").strip().upper()
    if not base_prefix.isalnum():
        print("❌ Invalid prefix. Must be alphanumeric.")
        exit(1)

    try:
        length = int(input(f"🔢 How many characters to match? (1-{len(base_prefix)}): "))
        assert 1 <= length <= len(base_prefix)
    except:
        print("❌ Invalid input. Defaulting to 4 characters.")
        length = 4

    use_leet = input("🎭 Enable 'leet-style' mode? (y/N): ").lower() == "y"

    target_prefix = base_prefix[:length]
    print(f"\n🎯 Searching for an address starting with something like: {target_prefix}")
    if use_leet:
        print("🌀 Leet mode enabled: will also search for variations like 3, 1, 0, etc.")

    variations_by_length = {}
    for i in range(length, 2, -1):
        variations_by_length[i] = generate_variations(target_prefix[:i], use_leet)

    best_matches = {i: None for i in variations_by_length}
    start_time = time.time()
    attempts = 0

    while True:
        mnemonic, pub, priv32, priv64 = generate_wallet()
        attempts += 1

        for i in variations_by_length:
            if any(pub.startswith(v) for v in variations_by_length[i]):
                if best_matches[i] is None or pub != best_matches[i]:
                    best_matches[i] = pub
                    elapsed = round(time.time() - start_time, 2)
                    print(f"\n🌟 New best match of {i} characters!")
                    print(f"📫 Public address: {pub}")
                    print(f"🔑 Private key (32b): {priv32}")
                    print(f"🔐 Extended private key (64b): {priv64}")
                    print(f"🧠 Mnemonic: {mnemonic}")
                    print(f"💾 Saved to: wallets_{base_prefix.lower()}_{i}.txt")

                    with open(f"wallets_{base_prefix.lower()}_{i}.txt", "a") as f:
                        f.write(f"{pub} | {priv32} | {mnemonic}\n")
                break

        if attempts % 10000 == 0:
            elapsed = time.time() - start_time
            hashrate = round(attempts / elapsed, 2)
            print(f"{attempts} attempts... last address: {pub} | ⛏️ {hashrate} addresses/sec")

