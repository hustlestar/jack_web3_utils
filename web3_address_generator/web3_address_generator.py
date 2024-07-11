import argparse
import time

from eth_account import Account
from eth_account.hdaccount import generate_mnemonic


def preprocess_address_starts(starts):
    processed = set()
    for start in starts:
        if start.lower().startswith("0x"):
            processed.add(start.lower()[2:])
        else:
            processed.add(start.lower())
    return processed


def generate_new_eth_address_with_seed_phrase(starts, ends, number_of_seed_phrase_words=12):
    Account.enable_unaudited_hdwallet_features()

    while True:
        seed_phrase = generate_mnemonic(num_words=number_of_seed_phrase_words, lang="english")
        account = Account.from_mnemonic(seed_phrase)
        address = account.address.lower()

        for start in starts:
            for end in ends:
                if address_matches(address, start, end):
                    return account, seed_phrase


def generate_new_eth_address_without_seed_phrase(starts, ends):
    while True:
        account = Account.create()
        seed_phrase = None
        address = account.address.lower()

        for start in starts:
            for end in ends:
                if address_matches(address, start, end):
                    return account, seed_phrase


def address_matches(address, start, end):
    return (not start or address.startswith("0x" + start)) and (not end or address.endswith(end))


def print_generation_result(address, key, seed_phrase):
    print(f"Address:      {address}")
    print(f"Private Key:  {key}")
    if seed_phrase:
        print(f"Seed Phrase:  {seed_phrase}")


def start_generation_job(starts, ends, number_of_addresses, use_seed_phrase, number_of_seed_phrase_words):
    results = []
    job_start_time = time.time()

    for i in range(number_of_addresses):
        print(f"Generating {i + 1} address")
        start_time = time.time()

        if use_seed_phrase:
            new_ethereum_account, seed_phrase = generate_new_eth_address_with_seed_phrase(starts, ends, number_of_seed_phrase_words)
        else:
            new_ethereum_account, seed_phrase = generate_new_eth_address_without_seed_phrase(starts, ends)

        results.append((new_ethereum_account.address, new_ethereum_account.key.hex(), seed_phrase))
        print_generation_result(new_ethereum_account.address, new_ethereum_account.key.hex(), seed_phrase)

        elapsed_time = time.time() - start_time
        print(f"Finished generation of {i + 1} address in {elapsed_time:.2f} seconds")

    print("-" * 100)
    for address, key, seed_phrase in results:
        print_generation_result(address, key, seed_phrase)
    job_elapsed_time = time.time() - job_start_time
    print("-" * 100)
    print(f"Job took : {job_elapsed_time:.2f} seconds")


def prepare_generation_job(ends, number_of_addresses, number_of_seed_phrase_words, starts, use_seed_phrase):
    starts = preprocess_address_starts(starts)
    ends = set(ends)
    print("-" * 100)
    accepted_address_starts = ', '.join(starts)
    accepted_address_ends = ', '.join(ends)
    print(f"Generating {number_of_addresses} Ethereum address(es) with the following parameters:"
          f"\nAddress starts: {{{accepted_address_starts}}}"
          f"\nAddress ends: {{{accepted_address_ends}}}"
          f"\nUse Seed Phrase: {'Enabled' if use_seed_phrase else 'Disabled'}"
          f"\nNumber of Seed Phrase Words: {number_of_seed_phrase_words}")
    print("-" * 100)
    return ends, starts


def generate_address(number_of_addresses, starts, ends, use_seed_phrase, number_of_seed_phrase_words):
    ends, starts = prepare_generation_job(ends, number_of_addresses, number_of_seed_phrase_words, starts, use_seed_phrase)
    start_generation_job(
        starts,
        ends,
        number_of_addresses,
        use_seed_phrase,
        number_of_seed_phrase_words,
    )


def main():
    parser = argparse.ArgumentParser(description="Generate new Ethereum address.")
    parser.add_argument("--address-start", nargs='+', default=[''],
                        help="Desired starts of the Ethereum address. May be several addresses separated by space.")
    parser.add_argument("--address-end", nargs='+', default=[''],
                        help="Desired ends of the Ethereum address. May be several addresses separated by space.")
    parser.add_argument("--number-of-addresses", type=int, default=1, help="Number of addresses to generate.")
    parser.add_argument("--use-seed-phrase", action='store_true', help="Enable seed phrase (it slows down generation significantly).")
    parser.add_argument("--number-of-seed-phrase-words", type=int, default=12, help="Number of words in the seed phrase, if enabled.")

    args = parser.parse_args()
    starts = args.address_start
    ends = args.address_end
    number_of_seed_phrase_words = args.number_of_seed_phrase_words
    number_of_addresses = args.number_of_addresses
    use_seed_phrase = args.use_seed_phrase

    generate_address(number_of_addresses, starts, ends, use_seed_phrase, number_of_seed_phrase_words)


if __name__ == "__main__":
    main()
