import argparse
import csv
import multiprocessing
import os.path
import time
from functools import partial

from eth_account import Account
from eth_account.hdaccount import generate_mnemonic

ADDR_CSV = 'addr.csv'


def load_existing_addresses():
    existing_addresses = set()
    if os.path.exists(ADDR_CSV):
        start_time = time.time()
        print("Loading existing addresses")
        with open(ADDR_CSV, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    existing_addresses.add(row[0].strip().lower())
        print(f"Loaded {len(existing_addresses)} addresses in {time.time() - start_time:.2f} seconds")
    return existing_addresses


def preprocess_address_starts(starts):
    processed = set()
    for start in starts:
        if start.lower().startswith("0x"):
            processed.add(start.lower()[2:])
        else:
            processed.add(start.lower())
    return processed


def generate_new_eth_address(starts, ends, existing_addresses, use_seed_phrase, number_of_seed_phrase_words=12):
    if use_seed_phrase:
        Account.enable_unaudited_hdwallet_features()

    while True:
        seed_phrase = generate_mnemonic(num_words=number_of_seed_phrase_words, lang="english")
        account = Account.from_mnemonic(seed_phrase)
        address = account.address.lower()

        if address in existing_addresses:
            print("|" * 100)
            print(f"Existing address found: {address}")
            print_generation_result(address, account.key.hex(), seed_phrase)
            print("|" * 100)
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


def check_existing_address(
        number_of_addresses,
        existing_addresses,
        starts,
        ends,
        use_seed_phrase,
        number_of_seed_phrase_words,
        generated_count,
        lock,
        process_number
):
    print(f"Starting process {process_number}")
    counter = 0
    while True:
        if counter % 10000 == 0:
            with lock:
                if generated_count.value >= number_of_addresses:
                    break
        account, seed_phrase = generate_new_eth_address(starts, ends, existing_addresses, use_seed_phrase, number_of_seed_phrase_words)
        print_generation_result(account.address.lower(), account.key.hex(), seed_phrase)
        with lock:
            generated_count.value += 1
            if generated_count.value >= number_of_addresses:
                break


def start_generation_job(starts, ends, number_of_addresses, use_seed_phrase, number_of_seed_phrase_words, address_set):
    job_start_time = time.time()

    cpu_count = multiprocessing.cpu_count() - 1
    print(f"Using {cpu_count} CPU cores")
    pool = multiprocessing.Pool(cpu_count)

    manager = multiprocessing.Manager()
    generated_count = manager.Value('i', 0)
    lock = manager.Lock()

    func = partial(
        check_existing_address,
        number_of_addresses,
        address_set,
        starts,
        ends,
        use_seed_phrase,
        number_of_seed_phrase_words,
        generated_count,
        lock
    )
    pool.map(func, range(cpu_count))
    pool.close()
    pool.join()

    job_elapsed_time = time.time() - job_start_time
    print("-" * 100)
    print(f"Job took : {job_elapsed_time:.2f} seconds")


def prepare_generation_job(ends, number_of_addresses, number_of_seed_phrase_words, starts, use_seed_phrase):
    starts = preprocess_address_starts(starts)
    ends = set(ends)
    existing_addresses = load_existing_addresses()

    print("-" * 100)
    accepted_address_starts = ', '.join(starts)
    accepted_address_ends = ', '.join(ends)
    print(f"Generating {number_of_addresses} Ethereum address(es) with the following parameters:"
          f"\nAddress starts: {{{accepted_address_starts}}}"
          f"\nAddress ends: {{{accepted_address_ends}}}"
          f"\nUse Seed Phrase: {'Enabled' if use_seed_phrase else 'Disabled'}"
          f"\nNumber of Seed Phrase Words: {number_of_seed_phrase_words}")
    print("-" * 100)
    return ends, starts, existing_addresses


def generate_address(number_of_addresses, starts, ends, use_seed_phrase, number_of_seed_phrase_words):
    ends, starts, existing_address_set = prepare_generation_job(ends, number_of_addresses, number_of_seed_phrase_words, starts, use_seed_phrase)
    start_generation_job(
        starts,
        ends,
        number_of_addresses,
        use_seed_phrase,
        number_of_seed_phrase_words,
        existing_address_set
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
